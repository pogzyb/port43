from textwrap import dedent

from langchain.prompts import PromptTemplate

WhoisTextToJson = PromptTemplate(
    input_variables=["data"],
    template=dedent(
        """Given the WHOIS data {data} about a domain name I want you to create a JSON formatted document containing
         the information as keys and values. The JSON document should follow this format:
    {{
    admin_address: $VALUE,
    admin_city: $VALUE,
    admin_country: $VALUE,
    admin_email: $VALUE,
    admin_fax: $VALUE,
    admin_id: $VALUE,
    admin_name: $VALUE,
    admin_organization: $VALUE,
    admin_phone: $VALUE,
    admin_state: $VALUE,
    admin_zipcode: $VALUE,
    billing_address: $VALUE,
    billing_city: $VALUE,
    billing_country: $VALUE,
    billing_email: $VALUE,
    billing_fax: $VALUE,
    billing_id: $VALUE,
    billing_name: $VALUE,
    billing_organization: $VALUE,
    billing_phone: $VALUE,
    billing_state: $VALUE,
    billing_zipcode: $VALUE,
    created: $VALUE,
    dnssec: $VALUE,
    domain_name: $VALUE,
    expires: $VALUE,
    name_servers: $VALUE,
    registrant_address: $VALUE,
    registrant_city: $VALUE,
    registrant_country: $VALUE,
    registrant_email: $VALUE,
    registrant_fax: $VALUE,
    registrant_name: $VALUE,
    registrant_organization: $VALUE,
    registrant_phone: $VALUE,
    registrant_state: $VALUE,
    registrant_zipcode: $VALUE,
    registrar: $VALUE,
    registrar_abuse_email: $VALUE,
    registrar_abuse_phone: $VALUE,
    registrar_iana_id: $VALUE,
    registrar_url: $VALUE,
    status: [$VALUE],
    tech_address: $VALUE,
    tech_city: $VALUE,
    tech_country: $VALUE,
    tech_email: $VALUE,
    tech_fax: $VALUE,
    tech_id: $VALUE,
    tech_name: $VALUE,
    tech_organization: $VALUE,
    tech_phone: $VALUE,
    tech_state: $VALUE,
    tech_zipcode: $VALUE,
    updated: $VALUE
}}
    where $VALUE is the value for the given key."""
    ),
)
