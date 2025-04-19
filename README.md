# Giới thiệu
Chương trình này bao gồm một backend (dùng FastAPI) và một frontend (dùng Node.js). Bạn có thể chạy chương trình theo hai cách: cục bộ (local) hoặc sử dụng Docker. Hãy làm theo các bước dưới đây để thiết lập và khởi động.

# Yêu cầu
- Cục bộ:
  - Python 3.11+

# Cách 1: Chạy cục bộ (Local)
1. Cài đặt backend
   
   1.1. Cài đặt các thư viện Python:

   ```
   cd backend
   pip install -r requirements.txt
   ```
 
   1.2. Cấu hình API key:
   - Tạo file .env trong thư mục backend/app/.env với nội dung tương tự như file .env.example.

   ```
   GOOGLE_API_KEY=your_gemini_api_key

   ```
   - Thay your_gemini_api_key bằng API key thực tế của Gemini.

   1.3. Chạy backend:

   ```
   cd app
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   - Backend sẽ chạy tại http://localhost:8000.