# ✈️ AI Trip Planner

> An intelligent travel planning platform powered by advanced AI agents. Create personalized itineraries, discover hidden gems, plan budgets, and explore destinations with real-time insights.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/) [![LangGraph](https://img.shields.io/badge/LangGraph-agentic--workflows-green)](https://langgraph.dev/) [![Streamlit](https://img.shields.io/badge/Streamlit-frontend-red)](https://streamlit.io/) [![FastAPI](https://img.shields.io/badge/FastAPI-backend-yellow)](https://fastapi.tiangolo.com/) [![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🎯 Overview

**AI Trip Planner** is a multi-agent agentic platform that leverages **LangGraph state machines** to orchestrate intelligent workflows for travel planning. It integrates specialized tool nodes for weather information, place search, expense calculation, and currency conversion—all accessible through a sleek **Streamlit interface** with a **FastAPI backend**.

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered Recommendations** | Intelligent travel suggestions tailored to your preferences |
| 📅 **Smart Itinerary Generation** | Auto-generate detailed day-by-day travel plans |
| 🗺️ **Destination Discovery** | Explore attractions, restaurants, and activities |
| 💰 **Budget Planning** | Real-time expense tracking and cost estimation |
| 🌤️ **Real-Time Information** | Live weather updates, events, and travel advisories |
| 💱 **Currency Conversion** | Instant exchange rates across global currencies |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (interactive conversational UI)
- **Backend**: FastAPI (REST API, microservices)
- **AI Orchestration**: LangGraph (agentic workflows, state machines)
- **LLM**: Groq, OpenAI, or other LLM providers
- **Tools**: Weather APIs, Place Search, Expense Calculators, Currency APIs
- **Language**: Python 3.8+

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- **Virtual environment** (recommended)

### Installation

**Step 1: Clone the repository**
```bash
git clone https://github.com/yourusername/AI_Trip_Planner.git
cd AI_Trip_Planner
```

**Step 2: Create a virtual environment**
```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Configure settings**
```bash
# Edit config/config.yaml with your API keys and preferences
nano config/config.yaml
```

### Running the Application

**Start the FastAPI backend:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**In a new terminal, launch the Streamlit frontend:**
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501` 🎉

---

## 📚 Project Structure

```
AI_Trip_Planner/
├── agent/
│   ├── __init__.py
│   └── agentic_workflow.py        # LangGraph orchestration logic
├── config/
│   ├── __init__.py
│   └── config.yaml                # Configuration settings
├── tools/
│   ├── __init__.py
│   ├── weather_info_tool.py        # Weather API integration
│   ├── place_search_tool.py        # Place search functionality
│   ├── expense_calculator_tool.py  # Budget & expense calculations
│   └── currency_conversion_tool.py # Currency conversion
├── utils/
│   ├── __init__.py
│   ├── model_loader.py             # LLM initialization
│   ├── config_loader.py            # Config utilities
│   ├── weather_info.py             # Weather utilities
│   ├── place_info_search.py        # Place search utilities
│   ├── expense_calculator.py       # Expense utilities
│   ├── currency_converter.py       # Currency utilities
│   └── save_to_document.py         # Document export
├── prompt_library/
│   ├── __init__.py
│   └── prompt.py                   # System prompts & templates
├── logger/
│   ├── __init__.py
│   └── logging.py                  # Logging configuration
├── exception/
│   ├── __init__.py
│   └── exeption_handling.py        # Error handling
├── main.py                         # FastAPI application entry point
├── streamlit_app.py                # Streamlit UI entry point
├── experiments.ipynb               # Development notebook
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Project metadata
└── README.md                       # You are here!
```

---

## 💻 Usage Example

### Using the Streamlit Interface

Simply open the app and chat naturally:
```
You: "I'm planning a 5-day trip to Paris with a $2000 budget. What should I see?"

AI Trip Planner: 
✈️ Day 1: Arrive in Paris, explore the Marais district...
🏨 Hotels: X, Y, Z - averaging $120/night
🍽️ Best restaurants near your hotels...
💰 Total estimated cost: $1,850
```

### Using the FastAPI Backend

```python
import requests

BASE_URL = "http://localhost:8000"

response = requests.post(f"{BASE_URL}/plan-trip", json={
    "destination": "Paris",
    "days": 5,
    "budget": 2000,
    "interests": ["art", "cuisine", "history"]
})

itinerary = response.json()
print(itinerary)
```

---

## 🔧 Configuration

Edit `config/config.yaml` to customize:

```yaml
llm:
  provider: "groq"        # Choose: groq, openai, etc.
  api_key: "${LLM_API_KEY}"

tools:
  weather_api_key: "${WEATHER_API_KEY}"
  place_search_key: "${PLACE_API_KEY}"
  currency_api_key: "${CURRENCY_API_KEY}"

interface:
  port: 8501
  host: "localhost"
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

For major changes, please **open an issue first** to discuss proposed changes.

---

## 📦 Dependencies

See `requirements.txt` for all dependencies. Key packages:

- `langgraph` - Agentic workflow orchestration
- `streamlit` - Interactive UI framework
- `fastapi` - Web framework
- `langchain` - LLM integrations
- `pydantic` - Data validation

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## � Deployment Guide

### Easiest Way: Free Tier Hosting - Render (All-in-One)

#### **Step 1: Prepare Your Repository**

```bash
# Make sure you have requirements.txt
pip freeze > requirements.txt

# Push to GitHub
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### **Step 2: Deploy Backend on Render**

1. **Go to [Render.com](https://render.com)** → Sign up with GitHub
2. **New → Web Service**
3. **Select your `AI_Trip_Planner` repository**
4. **Configure:**
   - **Name:** `ai-trip-planner-backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 8080`
5. **Add Environment Variables:**
   ```
   LLM_API_KEY = your_groq_api_key
   WEATHER_API_KEY = your_weather_api_key
   PLACE_API_KEY = your_place_search_api_key
   CURRENCY_API_KEY = your_currency_api_key
   ```
6. **Click Deploy** 🚀 → Copy your backend URL (e.g., `https://ai-trip-planner-backend.onrender.com`)

#### **Step 3: Deploy Frontend on Render**

1. **New → Web Service** (in Render dashboard)
2. **Select the same repository**
3. **Configure:**
   - **Name:** `ai-trip-planner-frontend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0`
4. **Add Environment Variable:**
   ```
   BACKEND_URL = https://ai-trip-planner-backend.onrender.com
   ```
5. **Click Deploy** 🚀

#### **Step 4: Update Your Frontend Code**

Edit `streamlit_app.py`:

```python
import os
import streamlit as st

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8080")

st.set_page_config(
    page_title="Voyager — AI Travel Planner",
    page_icon="✈️",
    layout="centered",
)
# Rest of your app...
```

#### **Step 5: Fix CORS in `main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Rest of your routes...
```

### ✅ Live & Free!

- **Frontend:** `https://ai-trip-planner-frontend.onrender.com` ✨
- **Backend:** `https://ai-trip-planner-backend.onrender.com` ⚙️
- **Cost:** $0 (with free tier limitations)

---

### Post-Deployment Checklist

- [ ] Set all API keys as **environment variables** (never hardcode!)
- [ ] Test the deployed app: `https://ai-trip-planner-frontend.onrender.com`
- [ ] Check backend logs for errors
- [ ] Verify all API keys are set as environment variables
- [ ] Test a full trip planning request
- [ ] Share the link with friends! 🎉

---

## �🆘 Support & Contact

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for ideas and questions
- **Email**: [your-email@example.com](mailto:hardickchatterjee2@gmail.com)

---

## 🙏 Acknowledgments

- Built with [LangGraph](https://langgraph.dev/) for intelligent agent orchestration
- UI powered by [Streamlit](https://streamlit.io/)
- Backend powered by [FastAPI](https://fastapi.tiangolo.com/)

---

<div align="center">

**Made with ❤️ for travelers and AI enthusiasts**

[⬆ back to top](#-ai-trip-planner)

</div>