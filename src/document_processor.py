import os
from pypdf import PdfReader
import docx
from typing import List
from config import Config
from langchain_experimental.text_splitter import SemanticChunker
from langchain_nvidia_ai_endpoints.embeddings import NVIDIAEmbeddings

class ExtractFile:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.file_extension = os.path.splitext(file_path)[1].lower()
        self.text = ""

    def _read_pdf(self) -> None:
        file_pdf = PdfReader(self.file_path)
        # duyet qua cac trang pdf
        for page in file_pdf.pages:
            # giai nen trang
            page = page.extract_text()
            if page:
                self.text += page + "\n"
        self.text = self.text.strip()

    def _read_docx(self) -> None:
        file_docx = docx.Document(self.file_path)
        # duyet tung paragraph cua work
        for paragraph in file_docx.paragraphs:
            if paragraph.text:
                self.text += paragraph.text + "\n"
        self.text = self.text.strip()

    def extract(self) -> None:
        if self.file_extension == ".pdf":
            self._read_pdf()
        elif self.file_extension == ".docx":
            self._read_docx()
        else:
            raise ValueError(f"Định dạng file {self.file_extension} không được hỗ trợ. Chỉ nhận .pdf hoặc .docx")
        
class Chunks:
    def __init__(self, text: str) -> None:
        self.embedding = NVIDIAEmbeddings(
            model=Config.NVIDIA_MODEL_EMBEDDING,
            nvidia_api_key=Config.NVIDIA_API_KEY,
            base_url=Config.NVIDIA_BASE_URL
        )
        self.text = text
        self.chunks: List[str] = []

    def split_to_chunk(self) -> None:
        # chia chunks
        text_splitter = SemanticChunker(
            embeddings=self.embedding,
            breakpoint_threshold_amount=0.85
        )
        self.chunks = text_splitter.split_text(self.text)
