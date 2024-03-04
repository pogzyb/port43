from pprint import pprint

from langchain.agents import AgentExecutor
from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser
from langchain.agents.format_scratchpad import format_log_to_messages
from langchain.schema import AIMessage, HumanMessage
from langchain_community.chat_models import ChatOllama
from src.port43 import get_react_json_prompt
from src.port43.tools import DNSTool, WHOISTool


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
    prompt = get_react_json_prompt(tools)
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
            {"input": "Who is the registrar for the domain name google.com?"}
        )
    )

"""
> Entering new AgentExecutor chain...
 Thought: I need to find out who the registrar is for the domain name google.com. I will use the whois_search tool to get this information.
Action: ```json
{
    "action": "whois_search",
    "action_input": "google.com"
}
```Domain Name: google.com
Registry Domain ID: 2138514_DOMAIN_COM-VRSN
Registrar WHOIS Server: whois.markmonitor.com
Registrar URL: http://www.markmonitor.com
Updated Date: 2019-09-09T15:39:04+0000
Creation Date: 1997-09-15T07:00:00+0000
Registrar Registration Expiration Date: 2028-09-13T07:00:00+0000
Registrar: MarkMonitor, Inc.
Registrar IANA ID: 292
Registrar Abuse Contact Email: abusecomplaints@markmonitor.com
Registrar Abuse Contact Phone: +1.2086851750
Domain Status: clientUpdateProhibited (https://www.icann.org/epp#clientUpdateProhibited)
Domain Status: clientTransferProhibited (https://www.icann.org/epp#clientTransferProhibited)
Domain Status: clientDeleteProhibited (https://www.icann.org/epp#clientDeleteProhibited)
Domain Status: serverUpdateProhibited (https://www.icann.org/epp#serverUpdateProhibited)
Domain Status: serverTransferProhibited (https://www.icann.org/epp#serverTransferProhibited)
Domain Status: serverDeleteProhibited (https://www.icann.org/epp#serverDeleteProhibited)
Registrant Organization: Google LLC
Registrant State/Province: CA
Registrant Country: US
Registrant Email: Select Request Email Form at https://domains.markmonitor.com/whois/google.com
Admin Organization: Google LLC
Admin State/Province: CA
Admin Country: US
Admin Email: Select Request Email Form at https://domains.markmonitor.com/whois/google.com
Tech Organization: Google LLC
Tech State/Province: CA
Tech Country: US
Tech Email: Select Request Email Form at https://domains.markmonitor.com/whois/google.com
Name Server: ns1.google.com
Name Server: ns3.google.com
Name Server: ns2.google.com
Name Server: ns4.google.com
DNSSEC: unsigned
URL of the ICANN WHOIS Data Problem Reporting System: http://wdprs.internic.net/
>>> Last update of WHOIS database: 2024-03-04T16:56:25+0000 <<<

For more information on WHOIS status codes, please visit:
  https://www.icann.org/resources/pages/epp-status-codes

If you wish to contact this domain’s Registrant, Administrative, or Technical
contact, and such email address is not visible above, you may do so via our web
form, pursuant to ICANN’s Temporary Specification. To verify that you are not a
robot, please enter your email address to receive a link to a page that
facilitates email communication with the relevant contact(s).

Web-based WHOIS:
  https://domains.markmonitor.com/whois

If you have a legitimate interest in viewing the non-public WHOIS details, send
your request and the reasons for your request to whoisrequest@markmonitor.com
and specify the domain name in the subject line. We will review that request and
may ask for supporting documentation and explanation.

The data in MarkMonitor’s WHOIS database is provided for information purposes,
and to assist persons in obtaining information about or related to a domain
name’s registration record. While MarkMonitor believes the data to be accurate,
the data is provided "as is" with no guarantee or warranties regarding its
accuracy.

By submitting a WHOIS query, you agree that you will use this data only for
lawful purposes and that, under no circumstances will you use this data to:
  (1) allow, enable, or otherwise support the transmission by email, telephone,
or facsimile of mass, unsolicited, commercial advertising, or spam; or
  (2) enable high volume, automated, or electronic processes that send queries,
data, or email to MarkMonitor (or its systems) or the domain name contacts (or
its systems).

MarkMonitor reserves the right to modify these terms at any time.

By submitting this query, you agree to abide by this policy.

MarkMonitor Domain Management(TM)
Protecting companies and consumers in a digital world.

Visit MarkMonitor at https://www.markmonitor.com
Contact us at +1.8007459229
In Europe, at +44.02032062220
--
 Thought: Based on the information obtained from the whois_search tool, the registrar for the domain name google.com is MarkMonitor, Inc.
Final Answer: The registrar for the domain name google.com is MarkMonitor, Inc.

> Finished chain.
{'input': 'Who is the registrar for the domain name google.com?',
 'output': 'The registrar for the domain name google.com is MarkMonitor, Inc.'}

"""
