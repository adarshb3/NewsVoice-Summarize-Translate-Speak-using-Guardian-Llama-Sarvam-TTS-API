import streamlit as st
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

# Load environment variables from .env file
load_dotenv()

# Fetch API keys
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
LLAMA_API_KEY = os.getenv("your_LLM_API_KEY")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

# Function to fetch news articles from The Guardian API
def fetch_news(api_key):
    from theguardian import theguardian_content
    content = theguardian_content.Content(api=api_key)
    raw_response = content.get_request_response()
    
    json_content = content.get_content_response()
    try:
        return content.get_results(json_content)
    except KeyError as e:
        st.error(f"Error fetching articles: {e}")
        return []

# Function to fetch article content
def fetch_article_content(article_url, api_key):
    response = requests.get(article_url, params={"api-key": api_key, "show-blocks": "all"})
    if response.status_code == 200:
        article_data = response.json()
        body = article_data.get("response", {}).get("content", {}).get("blocks", {}).get("body", [])
        if body:
            return " ".join(block.get("bodyTextSummary", "") for block in body)
    return None

# Function to summarize and translate content using Llama API
def summarize_and_translate(content, api_key, base_url="your_api_endpoint"):
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    summary_prompt = f"Summarize the following article content in 2-3 sentences:\n\n{content}\n\nSummary:"
    summary_response = client.completions.create(
        prompt=summary_prompt,
        temperature=0,
        model="your_model_name",
    )
    summary = summary_response.choices[0].text.strip()
    
    translation_prompt = f"Translate the following text to Punjabi:\n\n{summary}\n\nTranslation:"
    translation_response = client.completions.create(
        prompt=translation_prompt,
        temperature=0,
        model="your_model_name",
    )
    translation = translation_response.choices[0].text.strip()
    
    return summary, translation

# Function to convert Punjabi text to speech using Sarvam TTS API
def punjabi_text_to_speech(punjabi_text, sarvam_api_key):
    url = "https://api.sarvam.ai/text-to-speech"

    # Split text into chunks of up to 500 characters
    chunks = [punjabi_text[i:i+500] for i in range(0, len(punjabi_text), 500)]
    audio_clips = []

    for i, chunk in enumerate(chunks):
        payload = {
            "inputs": [chunk],
            "target_language_code": "pa-IN",
            "speaker": "meera",
            "pitch": 0,
            "pace": 1.0,
            "loudness": 1.2,
            "speech_sample_rate": 8000,
            "enable_preprocessing": True,
            "model": "bulbul:v1"
        }
        headers = {
            "Content-Type": "application/json",
            "API-Subscription-Key": sarvam_api_key
        }

        response = requests.post(url, headers=headers, json=payload)

        # Debugging: Print the response content
        print(f"Chunk {i+1} Response Status Code: {response.status_code}")
        print(f"Chunk {i+1} Response JSON: {response.json()}")

        if response.status_code == 200:
            # Ensure the "audios" key exists and is non-empty
            audio_base64 = response.json().get("audios")
            if audio_base64 and len(audio_base64) > 0:
                audio_clips.append(audio_base64[0])
            else:
                st.error(f"No audio found in response for chunk {i+1}.")
                return None
        else:
            st.error(f"Failed to convert chunk {i+1} to speech: {response.status_code} - {response.text}")
            return None

    # Combine all Base64 audio chunks into a single string
    return "".join(audio_clips)

# Streamlit App
st.title("News Summarization and Punjabi Audio Generator")

st.write("This app fetches news articles, summarizes them, translates to Punjabi, and generates audio.")

if st.button("Fetch and Process News"):
    st.write("Fetching news articles...")
    articles = fetch_news(GUARDIAN_API_KEY)

    if not articles:
        st.write("No articles found.")
    else:
        for article in articles[:3]:  # Process top 3 articles
            english_title = article.get('webTitle', 'No title available')
            article_url = article.get('apiUrl')

            st.subheader(english_title)

            article_content = fetch_article_content(article_url, GUARDIAN_API_KEY) if article_url else None
            if not article_content:
                st.write("No content available for this article.")
                continue

            try:
                # Summarize and Translate
                summary, punjabi_translation = summarize_and_translate(article_content, LLAMA_API_KEY)
                st.write("Punjabi Translation of Content:", punjabi_translation)

                # Text-to-Speech
                st.write("Generating Punjabi audio...")
                audio_base64 = punjabi_text_to_speech(punjabi_translation, SARVAM_API_KEY)

                if audio_base64:
                    audio_bytes = base64.b64decode(audio_base64)
                    st.audio(audio_bytes, format="audio/wav")

            except Exception as e:
                st.error(f"Error processing article: {e}")
