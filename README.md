# NewsVoiceAI-Summarize-Translate-Speak-using-Guardian-Llama-Sarvam-TTS-API
A Streamlit app that fetches news, summarizes it, translates English to Punjabi, and generates Punjabi audio.

## Overview

**NewsVoiceAI** is designed to simplify the process of consuming news by converting live articles into audio in Punjabi. This app:
- Fetches live news articles using **The Guardian API**.
- Summarizes the content into concise paragraphs using **Llama 3.1 70B** endpoint(You can replace this with your OpenAI API key).
- Translates the summarized content into Punjabi.
- Generates high-quality audio in Punjabi using **Sarvam TTS API**.

This tool is perfect for individuals who prefer listening to the latest global news in Punjabi instead of reading long articles.

---

## Features

1. **Fetch Live News**:
   - Retrieves the latest news articles from The Guardian API.

2. **Summarization**:
   - Compresses lengthy articles into short, meaningful summaries using the Llama API.

3. **Translation**:
   - Translates the summarized content into Punjabi for regional accessibility.

4. **Text-to-Speech**:
   - Converts the translated Punjabi text into audio using Sarvam's high-quality TTS model.

5. **Interactive User Interface**:
   - Built using Streamlit for a seamless and user-friendly experience.

---

## How It Works

1. **Fetch News**:
   - Connects to The Guardian API to fetch the latest articles.
   - Extracts the content for further processing.

2. **Summarize**:
   - Sends the article content to the Llama API, which summarizes it into 2-3 sentences.

3. **Translate**:
   - Translates the summary into Punjabi using the Llama3.1 70B endpoint API.

4. **Generate Audio**:
   - Converts the translated Punjabi text into audio files using Sarvam TTS API.
   - Handles text chunking for larger inputs (max 500 characters per chunk).

---

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- API keys for:
  - **[The Guardian API](https://open-platform.theguardian.com/)**
  - **LLM API**
  - **[Sarvam TTS API](https://sarvam.ai/)**

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/adarshb3/NewsVoiceAI-Summarize-Translate-Speak-using-Guardian-Llama-Sarvam-TTS-API.git
   cd NewsVoiceAI-Summarize-Translate-Speak-using-Guardian-Llama-Sarvam-TTS-API
2. Install required dependencies:
   ```
   pip install -r requirements.txt
3. Clone the Guardian library: The app uses the theguardian-api-python library, which is not available on PyPI. You must manually clone and install it:
   ```
   git clone https://github.com/prabhath6/theguardian-api-python.git
   cd theguardian-api-python
4. Add your API keys to a .env file: Create a file named .env in the project directory and add the following:
   ```
   GUARDIAN_API_KEY=your_guardian_api_key
   LLAMA-CLOUD_or_OPENAI_API_KEY=your_llama_api_key
   SARVAM_API_KEY=your_sarvam_api_key
5. Run the Streamlit app:
   ```
   streamlit run app.py
### Usage
1. Open the app in your browser at http://localhost:8501.
2. Click the "Fetch and Process News" button to:
- Fetch the top 3 news articles.
- Summarize and translate the content into Punjabi.
- Generate and play audio for the translations.
3. Listen to the generated Punjabi audio directly within the app.

https://github.com/user-attachments/assets/c61a9fea-38ce-4fd9-ad63-d492782b01cc

### Known Issues and Limitations
1. Character Limit:
- The Sarvam TTS API only accepts 500 characters per request. The app splits text automatically but very large inputs might cause minor delays.

2.  Dependency on APIs:
- The app relies on external APIs, which may have rate limits or downtime.

3.  Translation Quality:
- The accuracy of the Punjabi translation depends on the LLM's capabilities.

### License
This project is licensed under the MIT License. See `LICENSE` for more details.


   
