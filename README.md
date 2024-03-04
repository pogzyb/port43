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
So in other words, WHOIS is "Fragile, unparseable, obsolete... and universally relied upon" - [netmeister.org](https://www.netmeister.org/blog/whois.html)

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
 '{\n'
 '  "admin_address": "University of Michigan -- ITD\\nITCS, Arbor Lakes\\n4251 '
 'Plymouth Road\\nAnn Arbor, MI 48105-2785\\nUSA",\n'
 '  "admin_city": "Ann Arbor",\n'
 '  "admin_country": "USA",\n'
 '  "admin_email": "domainreg@umich.edu",\n'
 '  "admin_fax": "+1.7347641817",\n'
 '  "admin_id": "",\n'
 '  "admin_name": "",\n'
 '  "admin_organization": "University of Michigan -- ITD",\n'
 '  "admin_phone": "+1.7347641817",\n'
 '  "admin_state": "",\n'
 '  "admin_zipcode": "48105-3640",\n'
 '  "billing_address": "University of Michigan -- ITD\\nITCS, Arbor '
 'Lakes\\n4251 Plymouth Road\\nAnn Arbor, MI 48105-3640\\nUSA",\n'
 '  "billing_city": "Ann Arbor",\n'
 '  "billing_country": "USA",\n'
 '  "billing_email": "",\n'
 '  "billing_fax": "+1.7347641817",\n'
 '  "billing_id": "",\n'
 '  "billing_name": "",\n'
 '  "billing_organization": "University of Michigan -- ITD",\n'
 '  "billing_phone": "+1.7347641817",\n'
 '  "billing_state": "",\n'
 '  "billing_zipcode": "48105-3640",\n'
 '  "created": "07-Oct-1985",\n'
 '  "dnssec": "",\n'
 '  "domain_name": "UMICH.EDU",\n'
 '  "expires": "31-Jul-2024",\n'
 '  "name_servers": [\n'
 '    "UMICH-EDU.DNS.UMICH.ORG",\n'
 '    "UMICH-EDU.DNS.UMICH.NET",\n'
 '    "UMICH-EDU.DNS.UMICH.COM"\n'
 '  ],\n'
 '  "registrant_address": "University of Michigan -- ITD\\nITCS, Arbor '
 'Lakes\\n4251 Plymouth Road\\nAnn Arbor, MI 48105-2785\\nUSA",\n'
 '  "registrant_city": "Ann Arbor",\n'
 '  "registrant_country": "USA",\n'
 '  "registrant_email": "",\n'
 '  "registrant_fax": "+1.7347641817",\n'
 '  "registrant_id": "",\n'
 '  "registrant_name": "",\n'
 '  "registrant_organization": "University of Michigan -- ITD",\n'
 '  "registrant_phone": "+1.7347641817",\n'
 '  "registrant_state": "",\n'
 '  "registrant_zipcode": "48105-2785",\n'
 '  "registrar": "",\n'
 '  "registrar_abuse_email": "",\n'
 '  "registrar_abuse_phone": "",\n'
 '  "registrar_iana_id": "",\n'
 '  "registrar_url": "",\n'
 '  "status": [\n'
 '    "active"\n'
 '  ],\n'
 '  "tech_address": "University of Michigan\\nITS, Arbor Lakes\\n4251 Plymouth '
 'Road\\nAnn Arbor, MI 48105-3640\\nUSA",\n'
 '  "tech_city": "Ann Arbor",\n'
 '  "tech_country": "USA",\n'
 '  "tech_email": "",\n'
 '  "tech_fax": "+1.7347641817",\n'
 '  "tech_id": "",\n'
 '  "tech_name": "",\n'
 '  "tech_organization": "University of Michigan",\n'
 '  "tech_phone": "+1.7347641817",\n'
 '  "tech_state": "",\n'
 '  "tech_zipcode": "48105-3640",\n'
 '  "updated": "04-Jan-2024"\n'
 '}\n'
```
</details>

This whois example is just scratching the surface of what kind of problems LLM's can tackle. 
Again, the goal of Port43 is to highlight more use-cases and expand AI-first information security workflows. 

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