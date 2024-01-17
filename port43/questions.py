class Questions:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_question_set() -> dict[str, str]:
        questions = {}
        for entity in ["registrant", "technical", "admin", "billing"]:
            entity_questions = [
                ("Who is the {entity} organization?", "organization"),
                ("What is the {entity} name?", "name"),
                ("What is the {entity} street address?", "address"),
                ("What is the {entity} state or province?", "state"),
                ("What is the {entity} country?", "country"),
                ("What is the {entity} email address?", "email"),
                ("What is the {entity} phone number?", "phone"),
                ("What is the {entity} fax?", "fax"),
            ]
            for question, item in entity_questions:
                questions[f"{entity}_{item}"] = question.format(entity=entity)
        questions["domain_name"] = "What is the domain name?"
        questions["status"] = "What is the status?"
        questions["created_date"] = "What is the creation date?"
        questions["expires_date"] = "What is the expiration date?"
        questions["updated_date"] = "What is the updated date?"
        questions["name_servers"] = "What are the name servers?"
        questions["whois_server"] = "What is the whois server?"
        questions["registrar"] = "Who is the registrar?"
        questions["abuse_contact"] = "What is the abuse contact?"
        return questions

    @classmethod
    def from_tld(cls, top_level_domain: str):
        return cls.create_question_set()
