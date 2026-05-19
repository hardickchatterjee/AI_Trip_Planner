import os
from langchain.tools import tool
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

class CurrencyInput(BaseModel):
    amount: float = Field(description="The amount to convert")
    from_currency: str = Field(description="The source currency code (e.g., USD, EUR, INR)")
    to_currency: str = Field(description="The target currency code (e.g., USD, EUR, INR)")

class CurrencyConverterTool:
    def __init__(self):
        load_dotenv()
        self.currency_converter_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for currency conversion"""
        @tool(args_schema=CurrencyInput)
        def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
            """Convert currency from one type to another"""
            # Placeholder conversion rates - replace with real API call
            rates = {
                "USD": 1.0,
                "EUR": 0.92,
                "INR": 83.12,
                "GBP": 0.79,
                "JPY": 149.50,
            }
            
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()
            
            if from_currency not in rates or to_currency not in rates:
                return f"Currency conversion not supported for {from_currency} or {to_currency}"
            
            converted = amount * (rates[to_currency] / rates[from_currency])
            return f"{amount} {from_currency} = {converted:.2f} {to_currency}"
        
        return [convert_currency]
