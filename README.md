[![PyPI version](https://badge.fury.io/py/port43.svg)](https://badge.fury.io/py/whodap)
![package workflow](https://github.com/pogzyb/port43/actions/workflows/python-package.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# 🤿 port43

⚠️ **[work-in-progess]**

A set of open-source Information Security tools for the 🦜🔗 LangChain framework

### Premise

Port43's mission is to help you build information security based Large Language Model applications 

A few use-cases include ...
- Enabling Threat and SOC Analysts to query SIEM's using natural language
- Parsing and extracting data from DNS, WHOIS, and RDAP queries
- Gathering HTML, favicons, certificates, or screenshots from phishing sites on the internet
- Connecting popular Information Security API's (shodan, virustotal, etc.) with LLM's

... or combining any or all of the steps above into a single workflow!

### Quickstart

Check out the `examples/` folder for each example's complete code.

#### Basic example: WHOIS

WHOIS is a query and response protocol that is used for querying databases 
that store an Internet resource's registered users or assignees - [Wikipedia](https://en.wikipedia.org/wiki/WHOIS)

Unlike the modern RDAP standard which uses a JSON schema, the format of WHOIS responses follow a semi-free text format. 
So in other words, WHOIS is ["Fragile, unparseable, obsolete... and universally relied upon"](https://www.netmeister.org/blog/whois.html)

In order to parse WHOIS text responses from different registrars into a set of standardized key-value pairs that can be 
used by applications many open-source libraries have implemented a combination of regular expressions and text mining 
techniques. Despite some success the amount of edge-cases or registrars with unconventional implementations has caused
an overall inconsistent feel for many developers wishing to integrate WHOIS data into their applications.

For example, here is the authoritative output of `whois umich.edu`, which doesn't necessary follow 
the conventional single line key:value format:
```
-------------------------------------------------------------

Domain Name: UMICH.EDU

Registrant:
	University of Michigan -- ITD
	ITCS, Arbor Lakes
	4251 Plymouth Road
	Ann Arbor, MI 48105-2785
	USA

Administrative Contact:
	Domain Admin
	University of Michigan
	ITS, Arbor Lakes
	4251 Plymouth Road
	Ann Arbor, MI 48105-3640
	USA
	+1.7347641817
	domainreg@umich.edu

Technical Contact:
	 
	University of Michigan
	ITS, Arbor Lakes
	4251 Plymouth Road
	Ann Arbor, MI 48105-3640
	USA
	+1.7347641817
	domainreg@umich.edu

Name Servers:
	UMICH-EDU.DNS.UMICH.COM
	UMICH-EDU.DNS.UMICH.ORG
	UMICH-EDU.DNS.UMICH.NET

Domain record activated:    07-Oct-1985
Domain record last updated: 04-Jan-2024
Domain expires:             31-Jul-2024

```

Fortunately, the ever-growing capabilities of LLM's have made it possible to frame this problem in terms of an "AI-assistant"
(aka ChatModel) leading to impressive results with zero pre- and post-processing.

Here is some example code:

```python
# get a blob of WHOIS text
text, _ = asyncwhois.whois("umich.edu", authoritative_only=True)
# craft a prompt to extract key/values from the whois text
# the prompt asks the LLM to take the text and convert it into a standardized JSON format
prompt = WhoisTextToJson  # port43.prompts.whois_text_to_json.py
# pull any open-source LLM from HuggingFace
# or use Ollama: model = llm = ChatOllama("mistral")
llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    huggingfacehub_api_token=<HF_API_TOKEN>,
    model_kwargs={"max_new_tokens": 2048},
)
# wrapper for HuggingFace LLM's
model = ChatHuggingFace(llm=llm)
# LCEL
chain = prompt | model | StrOutputParser()
# view the result
pprint(chain.invoke(input={"data": text}))
```
<details>
  <summary>View the Result</summary>
  
Note that there is absolutely no postprocessing of the LLM output. The LLM
was able to match all keys/values on its own. Further processing could be added to
convert timestamps, fill-in null values, or modify values for a specific use-case.

```json
{
  "admin_address": "University of Michigan -- ITD\\nITCS, Arbor Lakes\\n4251 Plymouth Road\\nAnn Arbor, MI 48105-2785\\nUSA",
  "admin_city": "Ann Arbor",
  "admin_country": "USA",
  "admin_email": "domainreg@umich.edu",
  "admin_fax": "+1.7347641817",
  "admin_id": "",
  "admin_name": "",
  "admin_organization": "University of Michigan -- ITD",
  "admin_phone": "+1.7347641817",
  "admin_state": "",
  "admin_zipcode": "48105-3640",
  "billing_address": "University of Michigan -- ITD\\nITCS, Arbor Lakes\\n4251 Plymouth Road\\nAnn Arbor, MI 48105-3640\\nUSA",
  "billing_city": "Ann Arbor",
  "billing_country": "USA",
  "billing_email": "",
  "billing_fax": "+1.7347641817",
  "billing_id": "",
  "billing_name": "",
  "billing_organization": "University of Michigan -- ITD",
  "billing_phone": "+1.7347641817",
  "billing_state": "",
  "billing_zipcode": "48105-3640",
  "created": "07-Oct-1985",
  "dnssec": "",
  "domain_name": "UMICH.EDU",
  "expires": "31-Jul-2024",
  "name_servers": [
    "UMICH-EDU.DNS.UMICH.ORG",
    "UMICH-EDU.DNS.UMICH.NET",
    "UMICH-EDU.DNS.UMICH.COM"
  ],
  "registrant_address": "University of Michigan -- ITD\\nITCS, Arbor Lakes\\n4251 Plymouth Road\\nAnn Arbor, MI 48105-2785\\nUSA",
  "registrant_city": "Ann Arbor",
  "registrant_country": "USA",
  "registrant_email": "",
  "registrant_fax": "+1.7347641817",
  "registrant_id": "",
  "registrant_name": "",
  "registrant_organization": "University of Michigan -- ITD",
  "registrant_phone": "+1.7347641817",
  "registrant_state": "",
  "registrant_zipcode": "48105-2785",
  "registrar": "",
  "registrar_abuse_email": "",
  "registrar_abuse_phone": "",
  "registrar_iana_id": "",
  "registrar_url": "",
  "status": [
    "active"
  ],
  "tech_address": "University of Michigan\\nITS, Arbor Lakes\\n4251 Plymouth Road\\nAnn Arbor, MI 48105-3640\\nUSA",
  "tech_city": "Ann Arbor",
  "tech_country": "USA",
  "tech_email": "",
  "tech_fax": "+1.7347641817",
  "tech_id": "",
  "tech_name": "",
  "tech_organization": "University of Michigan",
  "tech_phone": "+1.7347641817",
  "tech_state": "",
  "tech_zipcode": "48105-3640",
  "updated": "04-Jan-2024"
}
```
</details>

This whois example is just scratching the surface of what kind of problems LLM's can tackle. 
Again, the goal of Port43 is to highlight more use-cases and expand AI-first information security workflows. 

#### Basic Agent: Finding DNS Records

```python
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
```

<details>
  <summary>View the Result</summary>

`examples/scripts/basic_react_agent_01.py`

```python
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
```

</details>

#### Advanced use-case: Threat Hunting using Natural Language

```python
coming soon...
```

#### Advanced use-case: Domain Monitoring & Phishing Detection

```python
coming soon...
```

### Roadmap
- Continue to expand the number of Tools
  - common interface for SIEM query integrations (Splunk, Elasticsearch, SumoLogic, etc.)
  - popular infosec API's (shodan, virustotal, ..., etc.)
  - popular open-source cli libraries (dnstwist, ..., etc.)  
- Add examples for advanced use-cases
- Abstract some of the LangChain Agent setup