from typing import Optional, Type

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from src.port43.core.whois import get_whois, aget_whois


class WHOISQueryInput(BaseModel):
    search_term: str = Field(description="Should be a Domain name, IP address, or ASN")


class WHOISTool(BaseTool):
    name = "whois_search"
    description = "useful for when you need to answer questions about WHOIS"
    args_schema: Type[BaseModel] = WHOISQueryInput

    def _run(
        self, term: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return get_whois(term)

    async def _arun(
        self, term: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return await aget_whois(term)
