# port43

`port43` | AI-powered WHOIS parsing

### Premise

<b>This is a loosely maintained "pet project" for now.</b>

`port43` applies Artifical Intelligence to a legacy problem in the Networking field. That is, WHOIS information typically follows a semi-structured format. There have been recent steps towards standardization like the RDAP protocol, but a large portion of WHOIS servers have.

### Quickstart

#### Installation
`pip install port43`

#### Basic

##### python package
```
from pprint import pprint
import port43

whois = port43.Client()
output = whois("google.com")

pprint(output)
```

##### Command Line (coming soon)
`python -m port43 -q "how many days ago was bitcoin.org registered?"`
`python -m port43 -q "what's the asn for 8.8.8.8?"`
