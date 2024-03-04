from pprint import pprint

from langchain.agents import AgentExecutor
from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser
from langchain.agents.format_scratchpad import format_log_to_messages
from langchain.schema import AIMessage, HumanMessage
from langchain_community.chat_models import ChatOllama
from src.port43 import get_react_json_prompt
from src.port43.tools import DNSTool, WHOISTool

# This example is the same as basic_react_agent_00.py,
# the only difference is the "input"


def _format_chat_history(chat_history):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer


if __name__ == "__main__":
    # add some tools
    tools = [DNSTool(), WHOISTool()]
    # get the ReAct prompt
    prompt = get_react_json_prompt(tools, render_args=True)
    # init any LLM; in this example we're using mistral via Ollama
    # figure out how to use Ollama here: https://ollama.com
    llm = ChatOllama(model="mistral", temperature=0)
    # have the model stop after solving the exercise
    chat_model_with_stop = llm.bind(stop=["\nObservation"])
    # create the agent
    agent = (
        {
            "input": lambda x: x["input"],
            "chat_history": lambda x: (
                _format_chat_history(x["chat_history"]) if x.get("chat_history") else []
            ),
            "agent_scratchpad": lambda x: format_log_to_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | chat_model_with_stop
        | ReActJsonSingleInputOutputParser()
    )
    # create an executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    pprint(
        agent_executor.invoke(
            {
                "input": "How many DNS records does google.com have? What are the MX records?"
            }
        )
    )

"""
> Entering new AgentExecutor chain...
 Thought: I need to find out how many DNS records google.com has and what its MX records are. I can use the dns_search tool for this.
Action:```json
{
    "action": "dns_search",
    "action_input": {
        "hostname": "google.com"
    }
}
```{
  "A": "142.250.191.142",
  "NS": "ns4.google.com.",
  "SOA": "ns1.google.com. dns-admin.google.com. 611883130 900 900 1800 60",
  "MX": "10 smtp.google.com.",
  "TXT": "\"apple-domain-verification=30afIBcvSuDV2PLX\"",
  "AAAA": "2607:f8b0:4009:818::200e",
  "CAA": "0 issue \"pki.goog\""
} Observation: The DNS records for google.com include one A record, two NS records, one SOA record, one MX record, one TXT record, one AAAA record, and one CAA record. The MX record is "10 smtp.google.com."
Thought: I now have the information to answer the original question.
Final Answer: Google.com has a total of 7 DNS records, including 1 A record, 2 NS records, 1 SOA record, 1 MX record, 1 TXT record, 1 AAAA record, and 1 CAA record. The MX records are "10 smtp.google.com."

> Finished chain.
{'input': 'How many DNS records does google.com have? What are the MX records?',
 'output': 'Google.com has a total of 7 DNS records, including 1 A record, 2 '
           'NS records, 1 SOA record, 1 MX record, 1 TXT record, 1 AAAA '
           'record, and 1 CAA record. The MX records are "10 smtp.google.com."'}
"""
