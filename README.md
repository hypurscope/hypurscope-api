# 📌 Hypurscope Backend Application

This is the backend application for the **hyperscope** project built with **FastAPI** 🚀.  

## 🚀 Features  
- ✅ FastAPI-powered REST API  
- ✅ Auto-generated Swagger & ReDoc documentation  
- ✅ Asynchronous request handling  
- ✅ Modular project structure  
- ✅ Ready for Docker & deployment  

## 🛠 Tech Stack  
- **Python** (3.10+)  
- **FastAPI** (backend framework)  
- **Uvicorn** (ASGI server)  
- **Pydantic** (data validation)  
- **MongoDB** (Data storage)  

## 📦 Installation  

1. **Clone repo**  
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. Create a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux / Mac
   venv\Scripts\activate      # Windows

3. Install dependencies
   ```bash
   pip install -r requirements.txt
4.  Run the Application
   ```bash
   uvicorn src.main:app --reload
   ```
   Now open: http:\\localhost:8000\docs

## API Docs
   Fastapi provides interactive docs of the box;
   i. Swagger UI: https://hyper-e1nj.onrender.com/docs
   ii. Redoc: https://hyper-e1nj.onrender.com/redoc

   Endpoints:
   a. GET https://hyper-e1nj.onrender.com/api/user-info/{id}
   b. GET https://hyper-e1nj.onrender.com/api/defi
   c. GET https://hyper-e1nj.onrender.com/api/get-holder/{token}
   d. GET https://hyper-e1nj.onrender.com/api/get-spot-info
   e. POST /api/track-wallet/api/track-wallet

## Project Structure
   .
   ├── src/
   │   ├── routes/        # API endpoints
   │   ├── helpers/       # helper-functions
   │   ├── validator/     # Pydantic schemas
   │   ├── services/      # Business logic
   │   └── main.py        # Entry point
   ├── requirements.txt
   └── README.md
