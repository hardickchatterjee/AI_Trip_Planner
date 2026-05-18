from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
import traceback

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize graph once at startup
graph_builder = None
react_app = None

@app.on_event("startup")
async def startup_event():
    """Initialize the graph builder and app once at startup"""
    global graph_builder, react_app
    try:
        print("Initializing graph builder at startup...")
        graph_builder = GraphBuilder(model_provider="groq")
        react_app = graph_builder()
        
        # Generate and save graph visualization once
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        print("Graph builder initialized successfully")
    except Exception as e:
        print(f"Error initializing graph builder: {traceback.format_exc()}")
        raise

class QueryRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"status": "running"}

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    """Query the travel agent using the pre-initialized graph"""
    try:
        if react_app is None:
            return JSONResponse(
                status_code=500, 
                content={"error": "Graph builder not initialized"}
            )
        
        print(f"Processing query: {query.question}")
        
        # Reuse the same graph instance
        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        return {"answer": final_output}
    except Exception as e:
        print(f"Error processing query: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": str(e)})
