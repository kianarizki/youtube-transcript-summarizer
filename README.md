# YouTube Video Transcript Summarizer

Aplikasi sederhana untuk mengekstrak transcript YouTube dan membuat ringkasan menggunakan Google Gemini AI.

## Features

- Extract transcript dari video YouTube
- AI summary menggunakan Gemini
- Support multi-bahasa (auto-detect)
- Download transcript

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Buat file `.env`:**
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **Jalankan aplikasi:**
   ```bash
   uv run streamlit run app.py
   ```

## Usage

1. Buka `http://localhost:8501`
2. Masukkan URL YouTube
3. Klik "Show Raw Transcript" atau "Show Summary"

## Requirements

- Python 3.10+
- Google Gemini API key
- Video YouTube dengan captions

## Dependencies

- streamlit
- google-generativeai  
- youtube-transcript-api
- python-dotenv
