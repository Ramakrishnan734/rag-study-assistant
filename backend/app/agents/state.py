from typing import List
from typing_extensions import TypedDict


class RAGState(TypedDict):
    query: str
    chunks: List[dict]
    answer: str