from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config import Config, Prompt
from typing import List
from vector_service import VectorDatabase

class NVIDIA_LLM_service:
    def __init__(self) -> None:
        if not Config.NVIDIA_API_KEY:
            raise ValueError("LỖI: Chưa tìm thấy NVIDIA_API_KEY trong file .env!")
        self.api_key = Config.NVIDIA_API_KEY
        self.base_url = Config.NVIDIA_BASE_URL
        self.model_name = Config.NVIDIA_MODEL_NAME
        self.summarize_single_prompt = ChatPromptTemplate.from_messages([
            ("system", Prompt.SUMMARIZE_SINGLE_PROMPT)
        ])
        self.summarize_total_prompt = ChatPromptTemplate.from_messages([
            ("system", Prompt.SUMMARIZE_TOTAL_PROMPT)
        ])
        self.retrieve_prompt = ChatPromptTemplate.from_messages([
            ("system", Prompt.RETRIEVE_PROMPT)
        ])
        self.vectordb = VectorDatabase()
        self.retrieve = self.vectordb.vector_store.as_retriever(
            search_type='similarity_score_threshold',
            search_kwargs={
                "k": 5,
                "score_threshold": 0.2
            }
        )
        self.llm = ChatNVIDIA(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=0,
        )
        self.parser = StrOutputParser()

    def summarize_single_chunk(self, chunk_text: str) -> str:
        chain = self.summarize_single_prompt | self.llm | self.parser
        response = chain.invoke({
                "chunk_text": chunk_text
        })
        return response
    
    def summarize_total_chunks(self, chunks_list_text: List[str]) -> str:
        if len(chunks_list_text) == 1:
            return self.summarize_single_chunk(chunks_list_text[0])
        final_text = ""
        for i, chunk_text in enumerate(chunks_list_text):
            print(f"Đang tóm tắt đoạn {i+1}/{len(chunks_list_text)}...")
            final_text += self.summarize_single_chunk(chunk_text) + "\n"
        chain = self.summarize_total_prompt | self.llm | self.parser
        final_response = chain.invoke({
            "final_text": final_text
        })
        return final_response

    def retrieve_response(self, question):
        chain = (
            {
                "Context": self.retrieve,
                "Question": RunnablePassthrough()
            } 
            | self.retrieve_prompt 
            | self.llm 
            | self.parser
        )
        response = chain.invoke(question)
        return response