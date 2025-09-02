#!/bin/bash

# AI Doctor Assistant Setup Script

echo "🏥 Setting up AI Doctor Assistant..."

# Create virtual environment for backend
echo "📦 Setting up Python virtual environment..."
cd backend
python -m venv venv

# Activate virtual environment (Windows)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Set up database
echo "🗄️  Setting up database..."
echo "Please ensure PostgreSQL is running and create a database named 'ai_doctor_db'"
echo "You can do this by running: createdb ai_doctor_db"

# Go back to root
cd ..

# Install Node.js dependencies for frontend
echo "🌐 Installing Node.js dependencies..."
cd frontend
npm install

# Go back to root
cd ..

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "1. Start PostgreSQL service"
echo "2. In backend directory: uvicorn app.main:app --reload"
echo "3. In frontend directory: npm start"
echo ""
echo "📝 Don't forget to:"
echo "- Update backend/.env with your OpenAI API key"
echo "- Update database credentials if different"
echo "- Install Tesseract OCR for image processing"
echo ""
echo "🌐 Frontend will run on: http://localhost:3000"
echo "🔧 Backend API will run on: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"