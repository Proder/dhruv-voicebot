# Dhruv AI - Personal Voice Assistant

A sophisticated AI voice assistant powered by Google's Gemini AI and Edge TTS, representing Dhruv Shah's personal and professional journey.

## Features

- 🗣️ **Voice Input**: Speak directly to the assistant using the microphone
- 🎵 **Natural Speech Output**: High-quality voice responses using Edge TTS
- 💬 **Text Chat**: Type your questions and get conversational responses
- 📱 **Responsive Design**: Clean, modern interface optimized for all devices
- 🧠 **Intelligent Conversations**: Powered by Google Gemini AI

## Live Demo

🚀 **[Try Dhruv AI](https://your-app-url.streamlit.app)**

## Setup for Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/dhruv-ai-assistant.git
   cd dhruv-ai-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Deployment on Streamlit Cloud

1. Push your code to GitHub (excluding sensitive files via `.gitignore`)
2. Connect your GitHub repo to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your `GOOGLE_API_KEY` in the Streamlit Cloud secrets management
4. Deploy!

## Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 1.5 Flash
- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: Microsoft Edge TTS
- **Audio Processing**: Python audio libraries

## Features in Detail

### Voice Interaction
- Real-time speech recognition
- Natural voice synthesis with various voice options
- Seamless audio playback in the browser

### AI Personality
- Sophisticated conversational AI with defined personality traits
- Context-aware responses
- Professional and personal knowledge base

### User Experience
- Clean, intuitive interface
- Real-time processing indicators
- Persistent chat history during session

## Contributing

This is a personal project showcasing AI assistant capabilities. Feel free to fork and adapt for your own use cases.

## License

MIT License - feel free to use and modify as needed.

## Contact

For questions or collaboration opportunities, reach out through the assistant itself or visit [Dhruv's Portfolio](https://dhruvshah-portfolio.vercel.app/)

---
