import os
from pprint import pprint

import asyncwhois
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models import ChatHuggingFace
from langchain_core.output_parsers import StrOutputParser
from port43.prompts import WhoisTextToJson

# Don't want to make a HuggingFace account? You could also use Ollama locally.
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Unlike the modern RDAP standard which uses a JSON schema, the format of WHOIS responses follow
# a semi-free text format. In order to parse WHOIS text responses from different registrars into a set of standardized
# key-value pairs that can be used by applications many open-source libraries have implemented a combination of regular
# expressions and text mining techniques. Despite some success the amount of edge-cases or registrars with
# unconventional implementations has caused an overall inconsistent feel for many developers wishing to integrate
# WHOIS data into their applications.
if __name__ == "__main__":
    # get a blob of WHOIS text
    text, _ = asyncwhois.whois("bitcoin.org", authoritative_only=True)
    # craft a prompt to extract key/values from the whois text
    prompt = WhoisTextToJson()
    # pull any open-source LLM from HuggingFace
    llm = HuggingFaceHub(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        task="text-generation",
        huggingfacehub_api_token=HF_API_TOKEN,
        model_kwargs={
            "max_new_tokens": 512,
            "top_k": 30,
            "temperature": 0.1,
            "repetition_penalty": 1.03,
        },
    )
    # wrapper for HuggingFace LLM's
    model = ChatHuggingFace(llm=llm)
    # LCEL
    chain = prompt | model | StrOutputParser()
    # view the result
    pprint(chain.invoke(input={"data": text}))
