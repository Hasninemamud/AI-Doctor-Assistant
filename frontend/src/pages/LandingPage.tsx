import React from 'react';
import { Link } from 'react-router-dom';
import { 
  HeartIcon, 
  DocumentTextIcon, 
  UserGroupIcon,
  ShieldCheckIcon,
  ClockIcon,
  ChartBarIcon,
  ArrowRightIcon,
  CheckCircleIcon,
  CloudArrowUpIcon,
  CpuChipIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-medical-100">
      {/* Navigation Header */}
      <nav className="bg-white shadow-sm border-b border-medical-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <HeartIcon className="h-8 w-8 text-primary-600 mr-2" />
              <span className="text-xl font-bold text-medical-800">AI Doctor Assistant</span>
            </div>
            <div className="flex space-x-4">
              <Link 
                to="/login" 
                className="text-medical-600 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
              >
                Sign In
              </Link>
              <Link 
                to="/register" 
                className="btn-primary"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative py-16 sm:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-medical-900 mb-6">
              Your AI-Powered <span className="text-primary-600">Medical Assistant</span>
            </h1>
            <p className="text-xl sm:text-2xl text-medical-600 mb-8 max-w-4xl mx-auto leading-relaxed">
              Get intelligent primary-level medical guidance through advanced AI analysis of your health documents and symptoms. 
              Fast, secure, and designed to support your healthcare journey.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link to="/register" className="btn-primary text-lg px-8 py-4 flex items-center">
                Start Your Health Assessment
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </Link>
              <Link to="/login" className="btn-secondary text-lg px-8 py-4">
                Sign In to Continue
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Goals & Mission Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-medical-900 mb-4">
              Our Mission: Democratizing Healthcare Access
            </h2>
            <p className="text-lg text-medical-600 max-w-3xl mx-auto">
              We believe everyone deserves access to intelligent medical guidance. Our AI-powered platform provides 
              preliminary health assessments, helping you understand your symptoms and medical reports.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <UserGroupIcon className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold text-medical-900 mb-3">Accessible Healthcare</h3>
              <p className="text-medical-600">
                Bridge the gap between patients and healthcare providers with intelligent preliminary assessments 
                available 24/7 from anywhere.
              </p>
            </div>
            
            <div className="text-center p-6">
              <div className="bg-success-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <CpuChipIcon className="h-8 w-8 text-success-600" />
              </div>
              <h3 className="text-xl font-semibold text-medical-900 mb-3">AI-Powered Analysis</h3>
              <p className="text-medical-600">
                Leverage advanced artificial intelligence to analyze medical documents, symptoms, and provide 
                structured health insights with professional disclaimers.
              </p>
            </div>
            
            <div className="text-center p-6">
              <div className="bg-warning-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <ShieldCheckIcon className="h-8 w-8 text-warning-600" />
              </div>
              <h3 className="text-xl font-semibold text-medical-900 mb-3">Safe & Secure</h3>
              <p className="text-medical-600">
                Your health data is protected with enterprise-grade security. We maintain strict privacy standards 
                and never replace professional medical advice.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-16 bg-medical-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-medical-900 mb-4">
              How to Get Primary Level Treatment
            </h2>
            <p className="text-lg text-medical-600 max-w-3xl mx-auto">
              Follow these simple steps to receive intelligent medical guidance and support for your health concerns.
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="flex items-start">
                <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-4 mt-1">
                  1
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-medical-900 mb-2">Create Your Account</h3>
                  <p className="text-medical-600">
                    Sign up securely with your email and create a personal health profile. Your data is encrypted 
                    and protected with industry-standard security measures.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-4 mt-1">
                  2
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-medical-900 mb-2">Start a New Consultation</h3>
                  <p className="text-medical-600">
                    Begin by describing your symptoms, medical concerns, or health questions. Our structured 
                    symptom assessment helps gather comprehensive information.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-4 mt-1">
                  3
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-medical-900 mb-2">Upload Medical Documents</h3>
                  <p className="text-medical-600">
                    Share test reports, lab results, medical images, or any relevant health documents. 
                    Our AI processes multiple formats including PDFs and images.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-4 mt-1">
                  4
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-medical-900 mb-2">Receive AI Analysis</h3>
                  <p className="text-medical-600">
                    Get intelligent insights about your health data, potential concerns, and recommendations 
                    for next steps in your healthcare journey.
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="text-center">
                <DocumentTextIcon className="h-16 w-16 text-primary-600 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-medical-900 mb-4">Primary Level Care</h3>
                <p className="text-medical-600 mb-6">
                  Our AI provides preliminary health assessments comparable to initial consultations, 
                  helping you understand your condition and plan appropriate care.
                </p>
                <div className="space-y-3 text-left">
                  <div className="flex items-center">
                    <CheckCircleIcon className="h-5 w-5 text-success-600 mr-3" />
                    <span className="text-medical-700">Symptom analysis and severity assessment</span>
                  </div>
                  <div className="flex items-center">
                    <CheckCircleIcon className="h-5 w-5 text-success-600 mr-3" />
                    <span className="text-medical-700">Medical document interpretation</span>
                  </div>
                  <div className="flex items-center">
                    <CheckCircleIcon className="h-5 w-5 text-success-600 mr-3" />
                    <span className="text-medical-700">Emergency condition detection</span>
                  </div>
                  <div className="flex items-center">
                    <CheckCircleIcon className="h-5 w-5 text-success-600 mr-3" />
                    <span className="text-medical-700">Personalized health recommendations</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Document Upload Guide */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-medical-900 mb-4">
              How to Upload Your Medical Documents
            </h2>
            <p className="text-lg text-medical-600 max-w-3xl mx-auto">
              Our advanced AI can analyze various types of medical documents to provide comprehensive health insights.
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="card text-center">
              <CloudArrowUpIcon className="h-12 w-12 text-primary-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-medical-900 mb-3">Supported Formats</h3>
              <ul className="text-medical-600 space-y-2">
                <li>• PDF documents (lab reports, prescriptions)</li>
                <li>• Images (JPG, PNG - X-rays, scans)</li>
                <li>• Medical test results</li>
                <li>• Prescription documents</li>
                <li>• Doctor's notes and reports</li>
              </ul>
            </div>
            
            <div className="card text-center">
              <DocumentTextIcon className="h-12 w-12 text-success-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-medical-900 mb-3">Upload Process</h3>
              <div className="text-medical-600 space-y-2">
                <p>1. Click on "Upload Documents" during consultation</p>
                <p>2. Drag & drop files or browse from your device</p>
                <p>3. Add descriptions for each document</p>
                <p>4. Wait for AI processing and analysis</p>
                <p>5. Review integrated results with your symptoms</p>
              </div>
            </div>
            
            <div className="card text-center">
              <ShieldCheckIcon className="h-12 w-12 text-warning-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-medical-900 mb-3">Privacy & Security</h3>
              <div className="text-medical-600 space-y-2">
                <p>• All documents are encrypted in transit and at rest</p>
                <p>• No data sharing with third parties</p>
                <p>• Automatic deletion options available</p>
                <p>• HIPAA-compliant security standards</p>
                <p>• You control your data completely</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-medical-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-medical-900 mb-4">
              Comprehensive Health Management Features
            </h2>
            <p className="text-lg text-medical-600 max-w-3xl mx-auto">
              Everything you need to understand and manage your health in one intelligent platform.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="card">
              <ClockIcon className="h-8 w-8 text-primary-600 mb-4" />
              <h3 className="text-xl font-semibold text-medical-900 mb-3">24/7 Availability</h3>
              <p className="text-medical-600">
                Access health guidance anytime, anywhere. No appointments needed - get preliminary 
                medical insights whenever you need them.
              </p>
            </div>
            
            <div className="card">
              <ChartBarIcon className="h-8 w-8 text-success-600 mb-4" />
              <h3 className="text-xl font-semibold text-medical-900 mb-3">Timeline Analysis</h3>
              <p className="text-medical-600">
                Track your health progression over time with detailed timeline analysis of symptoms, 
                treatments, and outcomes.
              </p>
            </div>
            
            <div className="card">
              <ExclamationTriangleIcon className="h-8 w-8 text-danger-600 mb-4" />
              <h3 className="text-xl font-semibold text-medical-900 mb-3">Emergency Detection</h3>
              <p className="text-medical-600">
                Advanced AI algorithms can identify potentially serious conditions and recommend 
                immediate medical attention when necessary.
              </p>
            </div>
            
            <div className="card">
              <DocumentTextIcon className="h-8 w-8 text-warning-600 mb-4" />
              <h3 className="text-xl font-semibold text-medical-900 mb-3">Consultation History</h3>
              <p className="text-medical-600">
                Keep a complete record of all your health consultations, analyses, and recommendations 
                in one secure location.
              </p>
            </div>
            
            <div className="card">
              <CpuChipIcon className="h-8 w-8 text-primary-600 mb-4" />
              <h3 className="text-xl font-semibold text-medical-900 mb-3">AI-Powered Insights</h3>
              <p className="text-medical-600">
                Leverage cutting-edge artificial intelligence trained on medical knowledge to 
                understand your health data and symptoms.
              </p>
            </div>
            
            <div className="card">
              <UserGroupIcon className="h-8 w-8 text-success-600 mb-4" />
              <h3 className="text-xl font-semibold text-medical-900 mb-3">Care Coordination</h3>
              <p className="text-medical-600">
                Generate comprehensive reports to share with your healthcare providers for better 
                care coordination and informed decisions.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Medical Disclaimer */}
      <section className="py-16 bg-danger-50 border-t-4 border-danger-500">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <ExclamationTriangleIcon className="h-12 w-12 text-danger-600 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-danger-800 mb-4">Important Medical Disclaimer</h2>
            <div className="text-danger-700 space-y-4 text-left">
              <p className="font-semibold">
                This AI Doctor Assistant is designed for educational and informational purposes only. 
                It is NOT intended to replace professional medical advice, diagnosis, or treatment.
              </p>
              <ul className="space-y-2 ml-6">
                <li>• Always consult qualified healthcare professionals for medical concerns</li>
                <li>• Never rely solely on AI analysis for medical decisions</li>
                <li>• In medical emergencies, contact emergency services immediately</li>
                <li>• This system cannot replace qualified medical practitioners</li>
                <li>• AI analysis may contain errors and should be verified by professionals</li>
              </ul>
              <p className="font-semibold">
                The developers and operators assume no responsibility for medical decisions made 
                based on information provided by this application.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-primary-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to Take Control of Your Health?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Join thousands of users who are already using AI-powered health insights to better 
            understand their medical conditions and make informed healthcare decisions.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/register" 
              className="bg-white text-primary-600 hover:bg-primary-50 font-medium py-3 px-8 rounded-lg transition-colors duration-200 text-lg"
            >
              Get Started for Free
            </Link>
            <Link 
              to="/login" 
              className="border-2 border-white text-white hover:bg-white hover:text-primary-600 font-medium py-3 px-8 rounded-lg transition-colors duration-200 text-lg"
            >
              Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-medical-900 text-medical-300 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center mb-4">
              <HeartIcon className="h-6 w-6 text-primary-400 mr-2" />
              <span className="text-lg font-semibold text-white">AI Doctor Assistant</span>
            </div>
            <p className="text-sm">
              Empowering healthcare decisions through artificial intelligence. 
              Always consult healthcare professionals for medical advice.
            </p>
            <p className="text-xs mt-2">
              © 2024 AI Doctor Assistant. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;