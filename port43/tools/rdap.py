from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from src.port43.core.rdap import get_rdap, aget_rdap


class RDAPQueryInput(BaseModel):
    search_term: str = Field(description="Should be a Domain name, IP address, or ASN")


class RDAPTool(BaseTool):
    name = "rdap_search"
    description = "useful for when you need to answer questions about RDAP"
    args_schema: Type[BaseModel] = RDAPQueryInput

    def _run(
        self, term: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return get_rdap(term)

    async def _arun(
        self, term: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return await aget_rdap(term)
