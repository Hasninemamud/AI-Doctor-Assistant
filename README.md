# AI Doctor Assistant

[![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)]()
[![React](https://img.shields.io/badge/React-18+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)]()

A comprehensive AI-powered medical consultation platform that provides intelligent analysis of medical test reports and patient symptoms. Built with modern web technologies and integrated with OpenRouter API for advanced medical reasoning.

## Overview

The AI Doctor Assistant is a full-stack web application designed to assist healthcare workflows through intelligent document processing and symptom analysis. The system processes uploaded medical reports, analyzes patient symptoms, and provides structured medical insights while maintaining appropriate medical disclaimers and professional boundaries.

### Key Capabilities

- **Comprehensive Landing Page**: User-friendly introduction with detailed guidance on app usage
- **Medical Document Processing**: Advanced OCR and PDF extraction for test reports and medical images
- **Intelligent Symptom Analysis**: Structured symptom collection with severity assessment and timeline tracking
- **AI-Powered Medical Assessment**: Integration with OpenRouter API for medical reasoning and analysis
- **Emergency Detection**: Automated identification of potentially critical conditions with specialized models
- **Enhanced Consultation System**: Multi-step consultation process with timeline analysis
- **Comprehensive Medical History**: Patient data management and consultation tracking
- **Demo Health Cases**: Pre-built realistic medical scenarios for testing and demonstration
- **Professional Security**: JWT authentication with secure token management

## Architecture

### Technology Stack

**Backend**
- FastAPI with automatic OpenAPI documentation
- PostgreSQL with SQLAlchemy ORM
- JWT-based authentication system
- OpenRouter API integration with multiple AI models
- httpx for HTTP requests
- Pydantic for data validation
- Enhanced medical analysis with specialized models

**Frontend**
- React 18 with TypeScript
- Redux Toolkit for state management
- Tailwind CSS for styling
- React Hook Form for form management
- React Dropzone for file uploads
- Heroicons for consistent iconography
- Comprehensive landing page with user guidance

**Infrastructure**
- Docker containerization
- PostgreSQL database
- File storage system
- Environment-based configuration

## Installation

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Docker (optional, recommended)
- OpenRouter API key

### Quick Start with Docker

```bash
# Clone the repository
git clone <repository-url>
cd AI-Doctor-Assistant/BuildCreative

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Installation

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your configuration

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Start development server
npm start
```

## Configuration

### Environment Variables

#### Backend (.env)
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/ai_doctor_db
SECRET_KEY=your-secure-secret-key-minimum-32-characters
OPENROUTER_API_KEY=your-openrouter-api-key
MAX_FILE_SIZE=10485760
UPLOAD_DIRECTORY=./uploaded_files
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000
```

## API Documentation

### Core Endpoints

#### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/auth/refresh` - Token refresh

#### Consultations
- `POST /api/v1/consultations/` - Create new consultation
- `GET /api/v1/consultations/` - Retrieve user consultations
- `POST /api/v1/consultations/{id}/analyze` - Request AI analysis

#### Enhanced Consultations
- `POST /api/v1/enhanced-consultations/` - Create enhanced consultation
- `POST /api/v1/enhanced-consultations/{id}/timeline-analysis` - Timeline analysis
- `POST /api/v1/enhanced-consultations/{id}/specialized-analysis` - Specialized analysis

#### Timeline Management
- `POST /api/v1/consultations/{id}/timeline` - Add timeline entry
- `GET /api/v1/consultations/{id}/timeline` - Get consultation timeline

#### File Management
- `POST /api/v1/files/upload/{consultation_id}` - Upload medical documents
- `GET /api/v1/files/{file_id}` - Retrieve file information

### Interactive Documentation

Access comprehensive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage

### Getting Started

#### Landing Page
Visit the application at `http://localhost:3000/` to access the comprehensive landing page that provides:
- Detailed explanation of the app's goals and mission
- Step-by-step guidance on getting primary-level medical treatment
- Instructions for uploading medical documents
- Feature overview and usage guidelines
- Important medical disclaimers

#### User Journey
1. **Landing Page**: Learn about the app and its capabilities
2. **Registration/Login**: Create account or sign in
3. **Dashboard**: Access main application features
4. **New Consultation**: Start medical consultation process
5. **Document Upload**: Upload medical reports and test results
6. **AI Analysis**: Receive intelligent medical insights
7. **History**: Review past consultations and analyses

### Basic Workflow

1. **User Registration**: Create account with secure authentication
2. **Consultation Creation**: Initialize new medical consultation
3. **Document Upload**: Upload test reports and medical images
4. **Symptom Input**: Provide structured symptom information
5. **AI Analysis**: Receive intelligent medical assessment
6. **Review Results**: Access comprehensive analysis and recommendations

### Enhanced Features

- **Landing Page**: Comprehensive introduction and user guidance
- **Timeline Analysis**: Track medical progression over time with pattern detection
- **Specialized Analysis**: Domain-specific medical evaluations with multiple AI models
- **Emergency Detection**: Automated critical condition identification with rapid screening
- **Medical History**: Comprehensive patient data management with search and filtering
- **Demo Health Cases**: Pre-built realistic scenarios for testing (see DEMO_HEALTH_ISSUE.md)
- **Multi-Model AI**: Integration with multiple AI providers for reliable analysis
- **Pattern Recognition**: Advanced symptom clustering and temporal analysis

## Development

### Project Structure

```
BuildCreative/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── api/v1/            # API endpoints
│   │   ├── core/              # Core functionality
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── main.py            # Application entry point
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components (including LandingPage)
│   │   ├── store/             # Redux state management
│   │   ├── services/          # API services
│   │   └── types/             # TypeScript definitions
│   ├── public/                # Static assets and manifest
│   └── package.json           # Node.js dependencies
├── docker-compose.yml          # Container orchestration
├── DEMO_HEALTH_ISSUE.md        # Comprehensive demo case
├── HOW_TO_USE_DEMO.md          # Demo usage instructions
└── README.md                   # Documentation
```

## Demo and Testing

### Demo Health Issue
A comprehensive demo health case is provided to showcase the application's capabilities:

- **Patient Case**: Recurring headaches with visual disturbances (Sarah Johnson)
- **Timeline**: 3-week symptom progression with escalating severity
- **Documents**: Sample blood work, symptom diary, and blood pressure logs
- **Features Demonstrated**: Pattern detection, risk assessment, emergency flagging

See `DEMO_HEALTH_ISSUE.md` and `HOW_TO_USE_DEMO.md` for complete details.

### Testing

```bash
# Backend testing
cd backend
python -m pytest tests/ -v

# Frontend testing
cd frontend
npm test

# Integration testing
python test_main.py
```

## Deployment

### Production Checklist

- [ ] Configure secure SECRET_KEY
- [ ] Set up production database
- [ ] Configure OpenRouter API access
- [ ] Set up SSL certificates
- [ ] Configure CORS policies
- [ ] Set up monitoring and logging
- [ ] Configure automated backups
- [ ] Review security settings

### Docker Production

```bash
# Production deployment
export POSTGRES_PASSWORD=secure-password
export SECRET_KEY=production-secret-key
export OPENROUTER_API_KEY=your-api-key

docker-compose -f docker-compose.yml up -d
```

## Security

### Security Features

- JWT-based authentication with automatic token refresh
- Bcrypt password hashing
- Comprehensive input validation
- Secure file upload and processing
- CORS configuration
- Rate limiting protection

### Best Practices

- Regular security updates
- Secure environment variable management
- Database access controls
- File upload restrictions
- API rate limiting

## AI Features and Capabilities

### Multiple AI Model Integration
The system leverages OpenRouter API to access various AI models optimized for medical reasoning:
- **Primary Model**: openai/gpt-oss-120b:free
- **Backup Models**: microsoft/wizardlm-2-8x22b:free, meta-llama/llama-3.1-8b-instruct:free, google/gemma-2-9b-it:free
- **Fallback Mechanisms**: Automatic model switching for reliability

### Specialized Medical Analysis
- **Emergency Screening**: Rapid detection of critical conditions
- **Clinical Analysis**: Comprehensive differential diagnosis
- **Timeline Analysis**: Pattern detection and symptom progression tracking
- **Risk Assessment**: Structured risk level evaluation (low/moderate/high/critical)
- **Confidence Scoring**: AI confidence levels for each analysis

### Pattern Recognition
- **Symptom Clustering**: Related symptoms appearing together
- **Temporal Associations**: Time-based symptom relationships
- **Progressive Tracking**: Linear regression for worsening trends
- **Cyclical Detection**: Recurring pattern identification
- **Emergency Indicators**: Rapid onset detection within hour windows

## Medical Disclaimer

**IMPORTANT NOTICE**: This application is designed for educational and informational purposes only. It is not intended to replace professional medical advice, diagnosis, or treatment.

### Key Points

- Always consult qualified healthcare professionals for medical concerns
- Never rely solely on AI analysis for medical decisions
- In medical emergencies, contact emergency services immediately
- This system cannot replace qualified medical practitioners
- AI analysis may contain errors and should be verified by professionals

### Liability

The developers and operators assume no responsibility for medical decisions made based on information provided by this application.

## Contributing

We welcome contributions to improve the AI Doctor Assistant. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes with clear messages
4. Push to your branch
5. Submit a Pull Request

### Development Standards

- Follow existing code style and conventions
- Include comprehensive tests for new features
- Update documentation as needed
- Ensure all tests pass before submission

