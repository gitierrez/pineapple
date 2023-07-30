import base64
import datetime

from typing import Optional
from pydantic import BaseModel, validator, constr
from langchain.retrievers import ArxivRetriever


class DisplayedDocument(BaseModel):
    base64_pdf: str

    @classmethod
    def from_file(cls, file):
        bytes_data = file.getvalue()
        return cls(base64_pdf=base64.b64encode(bytes_data).decode('utf-8'))


class PineappleDocument(BaseModel):
    published: datetime.date
    title: str
    authors: list[constr(strip_whitespace=True)]
    summary: str
    content: str
    base64_pdf: Optional[str] = None

    @classmethod
    def from_arxiv_id(cls, arxiv_id: str):
        if arxiv_id.startswith('arXiv:'):
            arxiv_id = arxiv_id[6:]
        arxiv_retriever = ArxivRetriever(load_max_docs=1)
        doc = arxiv_retriever.get_relevant_documents(query=arxiv_id)[0]
        return cls(
            published=doc.metadata['Published'],
            title=doc.metadata['Title'],
            authors=doc.metadata['Authors'],
            summary=doc.metadata['Summary'],
            content=doc.page_content
        )

    @validator('authors', pre=True)
    def authors_to_list(cls, v):
        if isinstance(v, str):
            return v.split(',')
        return v
