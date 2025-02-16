# Telegram Bot with HuggingFace Integration

A Telegram bot that uses HuggingFace's API for natural language processing.

## Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file with:

```bash
TELEGRAM_TOKEN=your_telegram_token
HUGGINGFACE_API_KEY=your_huggingface_token
IS_PROD=false
```

## Running the Bot

```bash
python main.py
```

## Deployment on Render

1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy as a Web Service
