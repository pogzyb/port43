from typing import Any
import subprocess
import shutil

import tldextract
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

from .questions import Questions
from .utils import QueryError, split_context, chunk_context, softmax


class Client:
    def __init__(self, model, tokenizer, tldextract_obj=None) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.tldextract = tldextract_obj or tldextract.TLDExtract(cache_dir="/tmp")

    @classmethod
    def from_pretrained(cls, repo: str = "timpal0l/mdeberta-v3-base-squad2", **kwargs):
        tokenizer = AutoTokenizer.from_pretrained(repo)
        model = AutoModelForQuestionAnswering.from_pretrained(repo)
        return cls(model, tokenizer, **kwargs)

    def __call__(self, name: str, whois_text: str = None, **kwargs: Any) -> Any:
        # parse the name
        extract_result = self.tldextract(name)
        # get whois text
        if whois_text is None:
            whois_text = self._get_whois_context(extract_result.registered_domain)
        # prepare questions
        questions = Questions.from_tld(extract_result.suffix)
        # do question answering
        answers = self.ask_questions(whois_text, questions)
        # post process output
        return answers

    def _get_whois_context(self, domain: str) -> str:
        cmd = self.do_whois_command(domain)
        if cmd.returncode != 0:
            raise QueryError(
                f"Command, whois {domain}, returned non-zero. stderr: {cmd.stderr}"
            )
        else:
            return cmd.stdout.decode(errors="ignore")

    @staticmethod
    def do_whois_command(name: str):
        whois_exec = shutil.which("whois")
        if not whois_exec:
            raise FileNotFoundError("whois not found in $PATH")
        cmd = subprocess.run([whois_exec, "-HI", name], capture_output=True)
        return cmd

    def ask_questions(self, context: str, questions: dict) -> dict:
        answers = {}
        context_line_by_line = split_context(context, 160)
        context_chunks = chunk_context(context_line_by_line, 3, 1)
        for chunk in context_chunks:
            chunk = "\n".join(chunk)
            for key, question in questions.items():
                answer, score = self._answer(chunk, question)
                if answer:
                    if question not in answers:
                        answers[key] = (answer, score)
                    else:
                        if score > answers[question][1]:
                            answers[key] = (answer, score)
        return answers

    def _answer(self, context, question):
        inputs = self.tokenizer(
            question, context, return_tensors="pt", truncation=True, max_length=512
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        start_scores, end_scores = (
            softmax(outputs.start_logits)[0],
            softmax(outputs.end_logits)[0],
        )
        start_idx, end_idx = np.argmax(start_scores), np.argmax(end_scores)
        confidence_score = (start_scores[start_idx] + end_scores[end_idx]) / 2
        answer_ids = inputs.input_ids[0][start_idx : end_idx + 1]
        answer_tokens = self.tokenizer.convert_ids_to_tokens(answer_ids)
        answer = self.tokenizer.convert_tokens_to_string(answer_tokens)
        if answer != self.tokenizer.cls_token:
            return answer, confidence_score
        return None, confidence_score
