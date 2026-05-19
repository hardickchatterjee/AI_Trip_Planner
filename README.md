# ✈️ AI Trip Planner

> An intelligent travel planning platform powered by advanced AI agents. Create personalized itineraries, discover hidden gems, plan budgets, and explore destinations with real-time insights.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/) [![LangGraph](https://img.shields.io/badge/LangGraph-agentic--workflows-green)](https://langgraph.dev/) [![Streamlit](https://img.shields.io/badge/Streamlit-frontend-red)](https://streamlit.io/) [![FastAPI](https://img.shields.io/badge/FastAPI-backend-yellow)](https://fastapi.tiangolo.com/) [![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🌐 Live App

**Production:** [https://aitripplanner-ozf7-production.up.railway.app/](https://aitripplanner-ozf7-production.up.railway.app/)

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
| 🌤️ **Real-Time Information** | Live weather updates and travel advisories |
| 💱 **Currency Conversion** | Instant exchange rates across global currencies |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (interactive conversational UI)
- **Backend**: FastAPI (REST API)
- **AI Orchestration**: LangGraph (agentic workflows, state machines)
- **LLM**: Groq (`meta-llama/llama-4-scout-17b-16e-instruct`) or OpenAI (`o4-mini`)
- **Tools**: OpenWeatherMap, Google Places API, Tavily Search, ExchangeRate-API
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
git clone https://github.com/hardickchatterjee/AI_Trip_Planner.git
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

**Step 4: Set up environment variables**

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
GPLACES_API_KEY=your_google_places_api_key
TAVILY_API_KEY=your_tavily_api_key
EXCHANGE_RATE_API_KEY=your_exchangerate_api_key
BASE_URL=http://localhost:8000
```

### Running the Application

**Terminal 1 — Start the FastAPI backend:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Start the Streamlit frontend:**
```bash
streamlit run streamlit_app.py
```

The app opens at `http://localhost:8501` 🎉

**Testing the backend directly:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Plan a 3-day trip to Paris with a $1500 budget"}'
```

---

## 📚 Project Structure

```
AI_Trip_Planner/
├── agent/
│   ├── __init__.py
│   └── agentic_workflow.py        # LangGraph orchestration logic
├── config/
│   ├── __init__.py
│   └── config.yaml                # LLM model configuration
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

response = requests.post(f"{BASE_URL}/query", json={
    "question": "Plan a 5-day trip to Paris with a $2000 budget"
})

result = response.json()
print(result["answer"])
```

---

## 🔧 Configuration

`config/config.yaml` controls which LLM models are used:

```yaml
llm:
  openai:
    provider: "openai"
    model_name: "o4-mini"
  groq:
    provider: "groq"
    model_name: "meta-llama/llama-4-scout-17b-16e-instruct"
```

The active provider is selected at runtime via the `model_provider` parameter in `GraphBuilder` (defaults to `"groq"`).

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
- `langchain`, `langchain-groq`, `langchain-openai` - LLM integrations
- `pydantic` - Data validation

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🚢 Deployment Guide

The app is deployed on **Railway**. To deploy your own instance:

### Deploy on Railway

1. **Push your code to GitHub**
2. **Go to [Railway.app](https://railway.app)** → New Project → Deploy from GitHub repo
3. **Add two services** from the same repo: one for the backend, one for the frontend

**Backend service:**
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}`
- **Environment Variables:**
  ```
  GROQ_API_KEY=...
  OPENAI_API_KEY=...
  OPENWEATHERMAP_API_KEY=...
  GPLACES_API_KEY=...
  TAVILY_API_KEY=...
  EXCHANGE_RATE_API_KEY=...
  ```

**Frontend service:**
- **Start Command:** `streamlit run streamlit_app.py --server.port=${PORT:-8501} --server.address=0.0.0.0`
- **Environment Variables:**
  ```
  BASE_URL=https://<your-backend-railway-url>
  ```

### Post-Deployment Checklist

- [ ] All API keys set as environment variables (never hardcode)
- [ ] `BASE_URL` in frontend service points to the deployed backend URL
- [ ] Test a full trip planning request end-to-end
- [ ] Check service logs for errors

---

## 🆘 Support & Contact

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for ideas and questions
- **Email**: [hardickchatterjee2@gmail.com](mailto:hardickchatterjee2@gmail.com)

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
