@echo off
REM AI Doctor Assistant Setup Script for Windows

echo 🏥 Setting up AI Doctor Assistant...

REM Create virtual environment for backend
echo 📦 Setting up Python virtual environment...
cd backend
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install Python dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

REM Go back to root
cd ..

REM Install Node.js dependencies for frontend
echo 🌐 Installing Node.js dependencies...
cd frontend
npm install

REM Go back to root
cd ..

echo ✅ Setup complete!
echo.
echo 🚀 To start the application:
echo 1. Start PostgreSQL service
echo 2. In backend directory: uvicorn app.main:app --reload
echo 3. In frontend directory: npm start
echo.
echo 📝 Don't forget to:
echo - Update backend\.env with your OpenAI API key
echo - Update database credentials if different
echo - Install Tesseract OCR for image processing
echo.
echo 🌐 Frontend will run on: http://localhost:3000
echo 🔧 Backend API will run on: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs

pause