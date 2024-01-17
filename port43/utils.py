import numpy as np


def softmax(x):
    return np.exp(x) / sum(np.exp(x))


def chunk_context(sentences: list, chunk_size: int, stride: int):
    chunks = []
    num_sentences = len(sentences)
    for i in range(0, num_sentences, chunk_size - stride):
        chunk = sentences[i : i + chunk_size]
        chunks.append(chunk)
    return chunks


def split_context(context_string: str, buffer_size: int) -> list:
    context_lines = []
    buffer = ""
    for line in context_string.split("\n"):
        if line:
            if len(buffer + line) + 1 > buffer_size:
                context_lines.append(buffer)
                buffer = line
            else:
                buffer += " " + line
    return context_lines


class QueryError(Exception):
    ...
