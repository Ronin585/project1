# 💬 FAQ Chatbot (demo-bot)

A simple, professional chatbot powered by the ChatGPT API. Built with Flask.

## 🔧 Setup Instructions

1. **Clone or unzip the project** into your folder.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Add your api key in .env file**:
   OPENAI_API_KEY=your_api_key_here

4. **Run the app**:
   python main.py

## 📁 Project Structure

main.py: Flask backend with OpenAI integration

static/: CSS and logo files

templates/: Frontend (HTML&JS)

utils/helpers.py: Logging, saving chat history and other functions

.env: Your API key and bot behaviour (SYSTEM_PROMPT)

requirements.txt: Needed packages

## Includes:
chat saving (chat_history.txt & chat_history.json)
typing animation
token trimming
responsive design
professional layout
memory context
customizable logo, styles and colors
