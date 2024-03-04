from typing import Optional, Type

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from src.port43.core.dns import get_dns


class DNSQueryInput(BaseModel):
    hostname: str = Field(description="Should be a Hostname")


class DNSTool(BaseTool):
    name = "dns_search"
    description = "useful for when you need to answer questions about DNS"
    args_schema: Type[BaseModel] = DNSQueryInput

    def _run(
        self, hostname: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return get_dns(hostname)

    async def _arun(
        self,
        hostname: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("No async DNS method.")
