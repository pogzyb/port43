from .client import Client

__version__ = "0.1.0"


def query(x):
    port43_client = Client.from_pretrained()
    return port43_client(x)
