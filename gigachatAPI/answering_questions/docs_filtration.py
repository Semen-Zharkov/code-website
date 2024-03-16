from typing import Any
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.embeddings.gpt4all import GPT4AllEmbeddings
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from chromadb.config import Settings


def filter_docs(split_docs: list[Document], question: str, out_files_num=4) -> Any:
    vectorstore = Chroma.from_documents(documents=split_docs,
                                        embedding=SentenceTransformerEmbeddings(),)
    docs = vectorstore.similarity_search(question, k=out_files_num)

    return docs, vectorstore


# def filter_docs2(split_docs: list[Document], question: str, out_files_num=4) -> Any:
#     vectorstore = Chroma.from_documents(documents=split_docs, embedding=GPT4AllEmbeddings())
#     docs = vectorstore.similarity_search(question, k=out_files_num)
#
#     return docs


# def filter_docs_new(split_docs: list[Document], question: str, out_files_num=4) -> Any:
#     vectorizer = TfidfVectorizer()
#
#     split_docs = list(map(lambda x: x.page_content, split_docs))
#
#     tfidf_matrix = vectorizer.fit_transform(split_docs + [question])
#
#     cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
#
#     tfidf_matches = sorted(enumerate(cosine_similarities), key=lambda x: x[1], reverse=True)
#
#     docs = list(map(lambda x: Document(page_content=split_docs[x[0]]), tfidf_matches[:out_files_num]))
#
#     return docs

