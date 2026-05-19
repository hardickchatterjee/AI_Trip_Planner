import os
from langchain.tools import tool
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    operation: str = Field(description="The operation to perform: add, subtract, multiply, or divide")
    num1: float = Field(description="The first number")
    num2: float = Field(description="The second number")

class CalculatorTool:
    def __init__(self):
        load_dotenv()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator"""
        @tool(args_schema=CalculatorInput)
        def calculate(operation: str, num1: float, num2: float) -> str:
            """Perform basic arithmetic operations"""
            operation = operation.lower()
            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "divide":
                if num2 == 0:
                    return "Error: Division by zero"
                result = num1 / num2
            else:
                return f"Unknown operation: {operation}"
            return f"{num1} {operation} {num2} = {result}"
        
        return [calculate]
