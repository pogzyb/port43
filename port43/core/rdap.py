import asyncwhois


def get_rdap(term: str):
    q, _ = asyncwhois.rdap(term)
    return q


async def aget_rdap(term: str):
    q, _ = await asyncwhois.aio_rdap(term)
    return q
