from src.rag.retriever import retrieve
from src.rag.generator import generate_answer


def rag_answer(user_question: str):
    # get top 4 similar passages
    passages = retrieve(user_question, top_k=4)

    # generate final JSON answer
    result = generate_answer(user_question, passages)

    return result
