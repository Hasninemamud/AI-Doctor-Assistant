# AI Doctor Assistant

🏥 **A fully functional AI-powered medical consultation system built with FastAPI and React**

A comprehensive full-stack web application that provides medical analysis and emergency treatment recommendations based on uploaded test reports and patient symptoms. Built following modern software architecture principles and medical AI best practices.

## ✨ Features

- 🏥 **Medical Test Report Processing** - Upload and analyze PDF reports and medical images
- 🩺 **Intelligent Symptom Analysis** - Structured symptom collection with severity tracking
- 🤖 **AI-Powered Medical Assessment** - GPT-4 powered analysis with medical reasoning
- 🚨 **Emergency Detection** - Automated identification of critical conditions
- 📊 **Medical History Management** - Comprehensive patient data tracking
- 🔐 **Secure Authentication** - JWT-based user authentication with role management
- 📱 **Responsive Design** - Mobile-friendly interface with medical theme
- ⚡ **Real-time Processing** - Instant file processing and AI analysis

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Advanced ORM with async support
- **JWT Authentication** - Secure token-based auth
- **OpenAI GPT-4** - Advanced medical AI analysis
- **File Processing** - PDF extraction and OCR capabilities
- **Medical Data Parsing** - Structured medical information extraction

### Frontend (React + TypeScript)
- **React 18** - Modern UI library with hooks
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling with medical theme
- **Redux Toolkit** - Predictable state management
- **React Hook Form** - Performant form handling
- **Axios** - HTTP client with interceptors

## 📁 Project Structure

```
ai-doctor-assistant/
├── 📁 backend/                     # FastAPI Backend
│   ├── 📁 app/
│   │   ├── 📁 api/v1/              # API endpoints
│   │   │   ├── auth.py             # Authentication routes
│   │   │   ├── users.py            # User management
│   │   │   ├── consultations.py    # Medical consultations
│   │   │   └── files.py            # File upload/processing
│   │   ├── 📁 core/                # Core functionality
│   │   │   ├── config.py           # Configuration settings
│   │   │   ├── database.py         # Database connection
│   │   │   ├── security.py         # JWT & password handling
│   │   │   └── deps.py             # Dependencies
│   │   ├── 📁 models/              # Database models
│   │   │   └── models.py           # SQLAlchemy models
│   │   ├── 📁 schemas/             # Pydantic schemas
│   │   │   └── schemas.py          # Request/response models
│   │   ├── 📁 services/            # Business logic
│   │   │   ├── ai_service.py       # AI analysis service
│   │   │   └── file_service.py     # File processing
│   │   └── main.py                 # FastAPI application
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Container config
│   └── .env                        # Environment variables
├── 📁 frontend/                    # React Frontend
│   ├── 📁 src/
│   │   ├── 📁 components/          # Reusable components
│   │   │   ├── Layout.tsx          # Main layout
│   │   │   ├── Navbar.tsx          # Navigation
│   │   │   └── Sidebar.tsx         # Side navigation
│   │   ├── 📁 pages/               # Page components
│   │   │   ├── LoginPage.tsx       # Authentication
│   │   │   ├── DashboardPage.tsx   # Main dashboard
│   │   │   ├── ConsultationPage.tsx # Medical consultation
│   │   │   └── HistoryPage.tsx     # Consultation history
│   │   ├── 📁 store/               # Redux state management
│   │   │   ├── store.ts            # Store configuration
│   │   │   ├── authSlice.ts        # Authentication state
│   │   │   └── consultationSlice.ts # Consultation state
│   │   ├── 📁 services/            # API services
│   │   │   └── api.ts              # HTTP client
│   │   ├── 📁 types/               # TypeScript definitions
│   │   │   └── index.ts            # Type definitions
│   │   ├── App.tsx                 # Main app component
│   │   └── index.tsx               # React entry point
│   ├── package.json                # Node.js dependencies
│   ├── tailwind.config.js          # Tailwind configuration
│   └── .env                        # Environment variables
├── docker-compose.yml              # Multi-container setup
├── setup.bat / setup.sh            # Setup scripts
└── README.md                       # This file
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
./setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

#### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- OpenAI API Key
- Tesseract OCR (for image processing)

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configurations

# Start the server
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env if needed

# Start development server
npm start
```

#### Database Setup
```sql
-- Create PostgreSQL database
createdb ai_doctor_db

-- Tables will be created automatically on first run
```

### Option 3: Docker Deployment
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## 🔧 Configuration

### Backend Environment Variables
```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_doctor_db

# Security
SECRET_KEY=your-super-secret-key-min-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIRECTORY=./uploaded_files
```

### Frontend Environment Variables
```bash
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## 🎯 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Token refresh

### Consultations
- `POST /api/v1/consultations/` - Create consultation
- `GET /api/v1/consultations/` - Get user consultations
- `POST /api/v1/consultations/{id}/symptoms` - Submit symptoms
- `POST /api/v1/consultations/{id}/analyze` - AI analysis

### File Management
- `POST /api/v1/files/upload/{consultation_id}` - Upload test reports
- `GET /api/v1/files/{file_id}` - Get file info
- `DELETE /api/v1/files/{file_id}` - Delete file

### User Management
- `GET /api/v1/users/me` - Get user profile
- `PUT /api/v1/users/me` - Update profile
- `GET /api/v1/users/me/medical-history` - Get medical history

## 🎨 Frontend Features

### User Interface
- **Medical Theme** - Professional healthcare design
- **Responsive Layout** - Mobile-first approach
- **Accessibility** - WCAG 2.1 compliant
- **Dark/Light Mode** - User preference support

### Components
- **File Upload** - Drag-and-drop with validation
- **Symptom Forms** - Structured medical data collection
- **Analysis Display** - Rich visualization of AI results
- **Emergency Alerts** - Critical condition warnings

## 🧠 AI Analysis Features

### Medical Analysis Capabilities
- **Symptom Analysis** - Comprehensive symptom evaluation
- **Test Report Processing** - PDF and image extraction
- **Risk Assessment** - Automated risk level calculation
- **Emergency Detection** - Critical condition identification
- **Treatment Recommendations** - Evidence-based suggestions

### AI Model Integration
- **GPT-4 Integration** - Advanced medical reasoning
- **Structured Prompts** - Medical-specific prompt engineering
- **Confidence Scoring** - Reliability assessment
- **Disclaimer Handling** - Appropriate medical warnings

## 🛡️ Security Features

- **JWT Authentication** - Secure token-based auth
- **Password Hashing** - bcrypt encryption
- **Input Validation** - Comprehensive data validation
- **File Security** - Safe file upload and processing
- **Rate Limiting** - API abuse prevention
- **CORS Configuration** - Secure cross-origin requests

## 📱 Application Flow

1. **User Registration/Login** - Secure account creation
2. **Medical History Setup** - Optional comprehensive history
3. **Consultation Creation** - New medical consultation
4. **File Upload** - Test reports and medical images
5. **Symptom Description** - Structured symptom collection
6. **AI Analysis** - Automated medical assessment
7. **Results Review** - Comprehensive analysis results
8. **Emergency Handling** - Critical condition protocols

## 🌐 Deployment

### Production Checklist
- [ ] Set strong SECRET_KEY
- [ ] Configure production database
- [ ] Set up OpenAI API key
- [ ] Configure file storage (AWS S3)
- [ ] Set up SSL certificates
- [ ] Configure monitoring
- [ ] Set up backups
- [ ] Review security settings

### Docker Production
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📊 Monitoring & Logging

- **Application Logs** - Comprehensive logging
- **Performance Metrics** - Response time tracking
- **Error Tracking** - Automated error reporting
- **Health Checks** - System status monitoring

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚠️ Important Medical Disclaimer

**CRITICAL NOTICE**: This AI Doctor Assistant is for **educational and informational purposes only**. It is **NOT intended to be a substitute** for professional medical advice, diagnosis, or treatment.

### Key Points:
- **Always consult healthcare professionals** for medical concerns
- **Never rely solely on AI analysis** for medical decisions
- **In emergencies**, call emergency services immediately
- **This system cannot replace** qualified medical practitioners
- **AI analysis may contain errors** and should be verified

### Liability
The developers and operators of this system assume no responsibility for any medical decisions made based on the information provided by this application.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 👥 Support

For support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed description

---

**Built with ❤️ for healthcare innovation**