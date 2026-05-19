# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AI Trip Planner** is a multi-agent travel planning platform that uses LangGraph to orchestrate intelligent AI workflows. The application comprises two main components:

1. **FastAPI Backend** (`main.py`) - Exposes a `/query` endpoint that processes natural language requests
2. **Streamlit Frontend** (`streamlit_app.py`) - Interactive conversational UI for trip planning

The system is powered by LLMs (Groq or OpenAI) integrated with specialized tools for weather, place search, expense calculation, and currency conversion.

## Architecture

### Core Workflow: LangGraph Agent System

The application uses **LangGraph state machines** to build a reactive AI agent that orchestrates tool calls:

```
User Query → LLM (with tools bound) → Conditional Routing:
  ├─ If tool calls needed → Execute tools → Return to LLM
  └─ If complete → Return response to user
```

**Key files:**
- `agent/agentic_workflow.py` - `GraphBuilder` class that constructs the LangGraph state machine
- `prompt_library/prompt.py` - System prompt defining agent behavior (instructs agent to always use tools first)

### Tools Layer

Four tool categories are bound to the LLM:

1. **WeatherInfoTool** (`tools/weather_info_tool.py`)
   - `get_current_weather(city)` - OpenWeatherMap API integration
   - `get_weather_forecast(city)` - 5-day forecast

2. **PlaceSearchTool** (`tools/place_search_tool.py`)
   - `search_attractions(place)` - Google Places API (fallback: Tavily)
   - `search_restaurants(place)` - Google Places API (fallback: Tavily)
   - `search_activities(place)` - Google Places API (fallback: Tavily)
   - `search_transportation(place)` - Google Places API (fallback: Tavily)

3. **CalculatorTool** (`tools/expense_calculator_tool.py`)
   - `estimate_total_hotel_cost(price_per_night, total_days)`
   - `calculate_total_expense(*costs)`
   - `calculate_daily_expense_budget(total_cost, days)`

4. **CurrencyConverterTool** (`tools/currency_conversion_tool.py`)
   - `convert_currency(amount, from_currency, to_currency)` - ExchangeRate-API integration

**Utility implementations:**
- `utils/weather_info.py` - WeatherForecastTool class with OpenWeatherMap requests
- `utils/place_info_search.py` - GooglePlaceSearchTool and TavilyPlaceSearchTool classes
- `utils/expense_calculator.py` - Calculator class with basic arithmetic
- `utils/currency_converter.py` - CurrencyConverter class with API calls

### Model Loading & Configuration

- `utils/model_loader.py` - `ModelLoader` class that loads ChatGroq or ChatOpenAI based on config
- `utils/config_loader.py` - Reads `config/config.yaml` for LLM model names and API setup
- `config/config.yaml` - Specifies model names for Groq (`llama-3.3-70b-versatile`) and OpenAI (`o4-mini`)

### API & Frontend

- `main.py` - FastAPI app with `/query` POST endpoint. Receives `QueryRequest` (question string), instantiates a fresh `GraphBuilder`, builds the graph, and invokes it with the question.
- `streamlit_app.py` - Rich Streamlit UI with chat history, styled with custom CSS (gold/dark theme). Makes HTTP requests to `BASE_URL` backend endpoint.

### Supporting Infrastructure

- `utils/save_to_document.py` - Exports trip plans to markdown files with timestamp-based naming
- `exception/exeption_handling.py` - Placeholder for error handling
- `logger/logging.py` - Logging configuration (minimal)

## Development Workflow

### Local Setup

1. **Environment & Dependencies**
   ```bash
   python3 -m venv env
   source env/bin/activate  # or env\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   - Create or update `.env` file with required API keys:
     - `GROQ_API_KEY` - Groq API key
     - `OPENAI_API_KEY` - OpenAI API key (if using OpenAI model)
     - `OPENWEATHERMAP_API_KEY` - OpenWeather API key
     - `GPLACES_API_KEY` - Google Places API key
     - `TAVILY_API_KEY` - Tavily search API key
     - `EXCHANGE_RATE_API_KEY` - ExchangeRate-API key
     - `BASE_URL` - Backend URL (default: `http://localhost:8080`)

### Running the Application

**Terminal 1 - Start FastAPI backend:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
The server will run on `http://localhost:8000` with auto-reload on code changes.

**Terminal 2 - Start Streamlit frontend:**
```bash
streamlit run streamlit_app.py
```
The app opens at `http://localhost:8501` by default.

**Testing the Backend Directly:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Plan a 3-day trip to Paris with a $1500 budget"}'
```

### Building & Packaging

The project uses `setuptools`:
```bash
python setup.py install
```

Dependencies are managed in `requirements.txt` (pinned versions) and `setup.py` (which parses requirements.txt).

## Key Design Patterns & Conventions

### Tool Definition Pattern

Tools follow a consistent pattern across the codebase:

1. **Tool class** (e.g., `WeatherInfoTool`) in `tools/` directory
2. **Utility class** (e.g., `WeatherForecastTool`) in `utils/` directory handling API calls
3. **Tool wrapper methods** using `@tool` decorator from `langchain.tools`
4. **Tool list registration** in `GraphBuilder._setup_tools()` → bound to LLM via `llm.bind_tools()`

Example flow: `weather_info_tool.py` → `weather_info.py` (API logic) → `@tool` decorator → LangGraph integration

### State Management

- Uses **LangGraph MessagesState** for conversation history
- System prompt prepended to user messages: `[system_prompt] + user_messages`
- Graph routing: agent → tools (if needed) → agent → response

### Configuration Management

- **YAML-based config** (`config/config.yaml`) for model selection
- **Environment variables** (`.env`) for API keys and deployment settings

## Common Development Tasks

### Adding a New Tool

1. Create a utility class in `utils/` (e.g., `utils/new_service.py`) with API integration logic
2. Create a tool wrapper in `tools/` (e.g., `tools/new_tool.py`) with `@tool` decorated methods
3. Instantiate the tool class in `GraphBuilder.__init__()` and extend `self.tools` list
4. Tool is automatically bound to LLM and available in the agent

### Modifying the Agent Behavior

- Edit `prompt_library/prompt.py` `SYSTEM_PROMPT` to change agent instructions
- The prompt explicitly directs the agent to use tools for information gathering

### Switching LLM Providers

- Change `model_provider` parameter when instantiating `GraphBuilder(model_provider="openai")`
- Add corresponding configuration in `config/config.yaml`
- Update `utils/model_loader.py` if adding new provider support

### Debugging Graph Execution

- `main.py` currently saves graph as PNG: `react_app.get_graph().draw_mermaid_png()` → `my_graph.png`
- Use this to visualize the state machine and understand routing

## Dependencies & External Services

**Key Python packages:**
- `langgraph` - Agentic state machine orchestration
- `langchain`, `langchain-community`, `langchain-experimental` - LLM integrations
- `langchain_groq`, `langchain_openai` - Model providers
- `streamlit` - Interactive UI framework
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `python-dotenv` - Environment variable loading

**External APIs:**
- OpenWeatherMap (weather forecasts)
- Google Places API (attractions, restaurants, activities, transportation)
- Tavily Search (fallback for place searches)
- ExchangeRate-API (currency conversion)
- Groq / OpenAI (LLM inference)

## Known Issues & Quirks

1. **Graph Instantiation**: `main.py` creates a fresh `GraphBuilder` per request. This is intentional after a rollback (see git history: commits `dd10244` and `b7737ee`).

2. **API Key Variable Naming**: `OPENWEATHERMAP_API_KEY` in environment but referred to as `OPENWEATHER_API_KEY` in some contexts. Verify consistency when updating.

3. **Exception Handling**: `exception/exeption_handling.py` is minimal (typo in filename). Error handling is inline in main.py and tool wrappers.

4. **No Tests**: No automated test suite exists. Manual testing via Streamlit UI or curl recommended.

## Deployment Notes

The README includes Render.com deployment instructions (free tier). Key setup:
- **Backend**: `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}`
- **Frontend**: `streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0`
- **CORS**: Already configured in `main.py` to allow all origins

