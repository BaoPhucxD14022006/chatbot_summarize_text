from src.ai_service import NVIDIA_LLM_service
from src.document_processor import ExtractFile, Chunks
import os
import streamlit as st

def main():
    file_path = input("File path: ").strip()
    file_path = file_path.strip("'\"")
    if not os.path.exists(file_path):
        raise ValueError(f"Lỗi: Không tìm thấy file tại đường dẫn: {file_path}")
    try:
        extract_file = ExtractFile(file_path)
        print("\n[Bước 1/3] Đang đọc và trích xuất dữ liệu từ file...")
        extract_file.extract()
        print(f"       => Đã đọc xong. Tổng số ký tự thô: {len(extract_file.text)}")
        if not extract_file.text:
            print("File rỗng hoặc không thể trích xuất vui lòng kiểm tra lại file.")
            return
        print("\n[Bước 2/3] Đang tiến hành chia nhỏ văn bản thông minh...")
        chunks = Chunks(extract_file.text)
        chunks.split_to_chunk()
        print(f"       => Đã chia văn bản thành {len(chunks.chunks)} đoạn nhỏ (chunks).")
        print("\n[Bước 3/3] Khởi tạo AI Service và gửi yêu cầu tóm tắt...")
        ai_service = NVIDIA_LLM_service()
        final_summary = ai_service.summarize_total_chunks(chunks.chunks)
        print("\n" + "="*50)
        print("KẾT QUẢ TÓM TẮT CUỐI CÙNG:")
        print("="*50)
        print(final_summary)
        print("="*50)
    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình xử lý: {e}")



if __name__ == "__main__":
    main()