from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_pages(pages:List[dict],chunk_size:int=500,chunk_overlap:int =100)->List[dict]:
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks=[]
    chunk_id=0

    for page in pages :
        texts=splitter.split_text(page["text"])
        for text in texts:
            chunks.append({
                "chunk_id":chunk_id,
                "text":text,
                "page_number":page["page_number"]
            })
            chunk_id+=1
    return chunks