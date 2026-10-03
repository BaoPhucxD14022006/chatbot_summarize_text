# 📚 AI Document Summarizer & RAG Chatbot (Chatbot Tóm Tắt & Hỏi Đáp Tài Liệu)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-AI_Endpoints-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://build.nvidia.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://python.langchain.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector_Database-DC382D?style=for-the-badge)](https://qdrant.tech/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

Ứng dụng AI thông minh hỗ trợ trích xuất, phân tích, tóm tắt tài liệu tự động và hỏi đáp (RAG - Retrieval-Augmented Generation) dựa trên mô hình ngôn ngữ lớn **Meta LLaMA 3.1 70B Instruct** và **NVIDIA Nemotron Embeddings** thông qua nền tảng **NVIDIA AI Foundation Endpoints**.

---

## 🌟 Tính Năng Nổi Bật (Key Features)

- 📄 **Đọc đa định dạng tài liệu**: Tự động đọc và trích xuất nội dung văn bản từ các tệp **PDF** (`.pdf`) và **Word** (`.docx`).
- 🧠 **Phân đoạn ngữ nghĩa thông minh (Semantic Chunking)**:
  - Sử dụng mô hình `llama-nemotron-embed-vl-1b-v2` để tính toán sự tương đồng ngữ nghĩa giữa các câu.
  - Phân tách đoạn văn bản tự nhiên theo ngữ cảnh thay vì cắt ký tự máy móc.
- ⚡ **Tóm tắt văn bản đa tầng (Hierarchical / Map-Reduce Summarization)**:
  - Tóm tắt từng đoạn nhỏ độc lập (`summarize_single_chunk`).
  - Hợp nhất và tinh chỉnh thành bản tóm tắt tổng thể có cấu trúc mạch lạc, chuẩn tiếng Việt (`summarize_total_chunks`).
- 🔍 **Hỏi đáp thông minh dựa trên tài liệu (RAG)**:
  - Tích hợp cơ sở dữ liệu vector **Qdrant** lưu trữ cục bộ (`./data/qdrant`).
  - Truy vấn tìm kiếm tương đồng theo ngưỡng tin cậy (`similarity_score_threshold`).
  - Prompt kiểm soát nghiêm ngặt: **Chống ảo giác (Anti-hallucination)**, chỉ trả lời dựa trên ngữ cảnh được cung cấp.
- 💬 **Quản lý lịch sử hội thoại (Chat History Database)**:
  - Lưu trữ phiên hội thoại vào cơ sở dữ liệu SQLite nhẹ nhàng, hiệu quả.
  - Hỗ trợ truy xuất lịch sử gần nhất theo từng `session_id`.
- ⚙️ **Cấu hình & Quản lý Prompt tách biệt**:
  - Dễ dàng tinh chỉnh prompt hệ thống trong file `static/prompt.yaml` mà không cần can thiệp vào mã nguồn.

---

## 🏗️ Kiến Trúc Hệ Thống (Workflow)

```mermaid
flowchart TD
    A[Tài liệu đầu vào: .pdf / .docx] --> B[src/document_processor.py: ExtractFile]
    B --> C[Văn bản thô]
    C --> D[Semantic Chunking<br/>NVIDIA Embedding Model]
    D --> E[Danh sách các Chunks ngữ nghĩa]
    
    subgraph Tóm Tắt Đa Tầng (Summarization Pipeline)
        E --> F[Tóm tắt từng đoạn con<br/>LLaMA 3.1 70B Instruct]
        F --> G[Các bản tóm tắt thành phần]
        G --> H[Hợp nhất & Tạo bản tóm tắt cuối cùng]
        H --> I[Kết quả tóm tắt mạch lạc tiếng Việt]
    end

    subgraph Truy Vấn Ngữ Cảnh (RAG Pipeline)
        E --> J[Lưu vào Qdrant Vector Store]
        K[Câu hỏi người dùng] --> L[Retriever: Similarity Search]
        J --> L
        L --> M[Prompt kiểm soát ngữ cảnh & chống bịa]
        M --> N[LLaMA 3.1 70B Instruct]
        N --> O[Câu trả lời chính xác có trích dẫn]
    end
```

---

## 📁 Cấu Trúc Thư Mục Dự Án (Project Structure)

```text
chatbot_summarize_text/
│
├── data/                       # Thư mục chứa dữ liệu mẫu và cơ sở dữ liệu
│   ├── baomoihomnay.docx       # Dữ liệu tài liệu thử nghiệm (.docx)
│   ├── baomoihomnay.pdf        # Dữ liệu tài liệu thử nghiệm (.pdf)
│   └── truyen.pdf              # Sách/truyện mẫu (.pdf)
│
├── src/                        # Mã nguồn chính của hệ thống
│   ├── __init__.py
│   ├── ai_service.py           # Khởi tạo mô hình ChatNVIDIA, chuỗi tóm tắt & hỏi đáp
│   ├── database.py             # Quản lý cơ sở dữ liệu lịch sử chat (SQLite)
│   ├── document_processor.py   # Trích xuất PDF/DOCX & phân đoạn SemanticChunker
│   └── vector_service.py       # Quản lý Vector DB Qdrant & Embedding
│
├── static/                     # Tài nguyên cấu hình tĩnh
│   └── prompt.yaml             # Hệ thống các System Prompts (Tóm tắt đơn, tóm tắt tổng, RAG)
│
├── .gitignore                  # Cấu hình bỏ qua các file nhạy cảm (.env, cache, tmp)
├── app.py                      # Chương trình chính chạy luồng tóm tắt tài liệu (CLI)
├── config.py                   # Đọc biến môi trường (.env) và nạp prompt.yaml
├── requirements.txt            # Danh sách các thư viện phụ thuộc
└── README.md                   # Tài liệu hướng dẫn sử dụng dự án
```

---

## 🚀 Hướng Dẫn Cài Đặt (Installation)

### 1. Yêu cầu hệ thống
- **Python**: Phiên bản 3.10 trở lên.
- **NVIDIA API Key**: Đăng ký miễn phí tại [NVIDIA NIM / Build](https://build.nvidia.com/).

### 2. Clone dự án về máy
```bash
git clone https://github.com/BaoPhucxD14022006/chatbot_summarize_text.git
cd chatbot_summarize_text
```

### 3. Tạo môi trường ảo (Khuyến nghị)
- **Trên Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **Trên Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

> **Lưu ý bổ sung**: Để sử dụng đầy đủ tính năng Vector Database với Qdrant trong `src/vector_service.py`, bạn có thể cài thêm:
> ```bash
> pip install langchain-qdrant qdrant-client
> ```

---

## 🔑 Cấu Hình Biến Môi Trường (Environment Variables)

Tạo một file `.env` tại thư mục gốc của dự án (`chatbot_summarize_text/.env`) với nội dung sau:

```env
# API Key lấy từ https://build.nvidia.com/
NVIDIA_API_KEY=nvapi-your-nvidia-api-key-here
```

---

## 💻 Hướng Dẫn Sử Dụng (Usage)

### 1. Chạy chương trình tóm tắt qua giao diện dòng lệnh (CLI)
Khởi chạy tệp `app.py`:
```bash
python app.py
```

Quy trình hoạt động:
1. Nhập đường dẫn tới tệp tài liệu cần tóm tắt (ví dụ: `data/baomoihomnay.pdf` hoặc `data/baomoihomnay.docx`).
2. Hệ thống sẽ lần lượt:
   - **Bước 1/3**: Đọc và trích xuất toàn bộ văn bản.
   - **Bước 2/3**: Phân tách văn bản thành các chunks thông minh theo ngữ nghĩa.
   - **Bước 3/3**: Gọi mô hình AI thực hiện tóm tắt từng phần và hợp nhất thành bản tóm tắt cuối cùng.
3. Kết quả tóm tắt tiếng Việt hoàn chỉnh sẽ được in ra màn hình.

---

## 📝 Tùy Chỉnh Prompt (`static/prompt.yaml`)

Bạn có thể chỉnh sửa các tiêu chuẩn tóm tắt hoặc quy tắc trả lời trong `static/prompt.yaml`:
- **`summarize_single_prompt`**: Hướng dẫn cách AI tóm tắt từng đoạn văn ngắn.
- **`summarize_total_prompt`**: Tiêu chuẩn hợp nhất các đoạn tóm tắt thành văn bản hoàn chỉnh.
- **`retrieve_prompt`**: Các điều luật nghiêm ngặt khi trả lời câu hỏi tìm kiếm (chống bịa đặt, buộc trích dẫn).

---

## 🛠️ Công Nghệ Sử Dụng (Tech Stack)

| Thành phần | Công nghệ / Thư viện | Mô tả |
| :--- | :--- | :--- |
| **LLM Model** | `meta/llama-3.1-70b-instruct` | Mô hình ngôn ngữ lớn mạnh mẽ từ NVIDIA NIM |
| **Embeddings** | `llama-nemotron-embed-vl-1b-v2` | Mô hình nhúng ngữ nghĩa chuyên sâu của NVIDIA |
| **LLM Framework** | `LangChain`, `LangChain NVIDIA` | Xây dựng pipeline, Prompt template & Chains |
| **Text Splitter** | `SemanticChunker` (`langchain-experimental`) | Tách văn bản dựa trên khoảng cách ngữ nghĩa |
| **Document Parsers** | `pypdf`, `python-docx` | Đọc tài liệu định dạng PDF & Word |
| **Vector Database** | `Qdrant` (`qdrant-client`, `langchain-qdrant`) | Lưu trữ và tìm kiếm vector embeddings cục bộ |
| **Database** | `SQLite` | Lưu trữ lịch sử đoạn hội thoại của người dùng |
| **Frontend/UI** | `Streamlit` | Giao diện web tương tác trực quan (đang mở rộng) |

---

## 📌 Lộ Trình Phát Triển (Roadmap)

- [x] Trích xuất dữ liệu từ PDF và DOCX.
- [x] Phân đoạn Semantic Chunking với NVIDIA Embeddings.
- [x] Tóm tắt văn bản đa tầng Map-Reduce.
- [x] Xây dựng module Vector Database với Qdrant & Lưu lịch sử chat SQLite.
- [ ] Hoàn thiện giao diện Web trực quan bằng **Streamlit** (Upload file, chat tương tác thời gian thực).
- [ ] Bổ sung tính năng trích xuất hình ảnh và bảng biểu từ tài liệu.
- [ ] Hỗ trợ xuất kết quả tóm tắt ra file `.docx`, `.pdf`, `.md`.

---

## 👤 Tác Giả (Author)

- GitHub: [@BaoPhucxD14022006](https://github.com/BaoPhucxD14022006)
- Dự án: [chatbot_summarize_text](https://github.com/BaoPhucxD14022006/chatbot_summarize_text)
