import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { useForm } from 'react-hook-form';
import { useDropzone } from 'react-dropzone';
import toast from 'react-hot-toast';

import { AppDispatch, RootState } from '../store/store';
import {
  createConsultation,
  getConsultation,
  submitSymptoms,
  analyzeConsultation,
  uploadTestReport,
  clearError
} from '../store/consultationSlice';
import { SymptomData, Recommendation } from '../types';

interface SymptomFormData {
  chief_complaint: string;
  location: string;
  severity: number;
  duration: string;
  onset: string;
  quality: string;
  associated_symptoms: string;
  aggravating_factors: string;
  relieving_factors: string;
}

const ConsultationPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  const { currentConsultation, isLoading, isAnalyzing, analysis, error } = useSelector(
    (state: RootState) => state.consultation
  );

  const [currentStep, setCurrentStep] = useState<'create' | 'symptoms' | 'files' | 'analysis'>('create');
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<SymptomFormData>();

  // Initialize consultation
  useEffect(() => {
    if (id) {
      // Load existing consultation
      dispatch(getConsultation(id));
      setCurrentStep('symptoms');
    } else {
      // Create new consultation
      handleCreateConsultation();
    }
  }, [id, dispatch]);

  useEffect(() => {
    dispatch(clearError());
  }, [dispatch]);

  const handleCreateConsultation = async () => {
    try {
      const result = await dispatch(createConsultation()).unwrap();
      toast.success('New consultation created!');
      navigate(`/consultation/${result.id}`);
    } catch (error: any) {
      toast.error(error || 'Failed to create consultation');
    }
  };

  const onSubmitSymptoms = async (data: SymptomFormData) => {
    if (!currentConsultation?.id) return;

    try {
      const symptomsData = {
        chief_complaint: data.chief_complaint,
        symptoms: [{
          location: data.location,
          severity: data.severity,
          duration: data.duration,
          onset: data.onset,
          quality: data.quality,
          associated_symptoms: data.associated_symptoms.split(',').map(s => s.trim()).filter(Boolean),
          aggravating_factors: data.aggravating_factors.split(',').map(s => s.trim()).filter(Boolean),
          relieving_factors: data.relieving_factors.split(',').map(s => s.trim()).filter(Boolean)
        }]
      };

      await dispatch(submitSymptoms({ 
        id: currentConsultation.id, 
        symptoms: symptomsData 
      })).unwrap();
      
      toast.success('Symptoms submitted successfully!');
      setCurrentStep('files');
    } catch (error: any) {
      toast.error(error || 'Failed to submit symptoms');
    }
  };

  const handleFileUpload = async (files: File[]) => {
    if (!currentConsultation?.id) return;

    setUploadedFiles(prev => [...prev, ...files]);
    
    for (const file of files) {
      try {
        await dispatch(uploadTestReport({ 
          consultationId: currentConsultation.id, 
          file 
        })).unwrap();
        
        toast.success(`${file.name} uploaded successfully!`);
      } catch (error: any) {
        toast.error(`Failed to upload ${file.name}: ${error}`);
      }
    }
  };

  const handleAnalyze = async () => {
    if (!currentConsultation?.id) return;

    try {
      await dispatch(analyzeConsultation(currentConsultation.id)).unwrap();
      toast.success('Analysis completed!');
      setCurrentStep('analysis');
    } catch (error: any) {
      toast.error(error || 'Analysis failed');
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.jpg', '.jpeg', '.png']
    },
    maxSize: 10485760, // 10MB
    onDrop: handleFileUpload
  });

  if (!currentConsultation && currentStep !== 'create') {
    return (
      <div className="flex justify-center items-center min-h-64">
        <div className="spinner"></div>
        <span className="ml-2 text-medical-600">Loading consultation...</span>
      </div>
    );
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-4">
        <h1 className="text-xl sm:text-2xl font-bold text-medical-900">
          {id ? `Consultation #${id.slice(-8)}` : 'New Consultation'}
        </h1>
        <div className="flex items-center gap-2">
          {/* Enhanced Analysis Button */}
          {currentConsultation?.id && (
            <Link
              to={`/consultation/enhanced/${currentConsultation.id}`}
              className="btn btn-secondary text-xs sm:text-sm"
            >
              Enhanced Analysis
            </Link>
          )}
          {currentConsultation?.status && (
            <span className={`px-3 py-1 rounded-full text-xs sm:text-sm font-medium ${
              currentConsultation.status === 'draft' ? 'bg-warning-100 text-warning-800' :
              currentConsultation.status === 'active' ? 'bg-primary-100 text-primary-800' :
              currentConsultation.status === 'completed' ? 'bg-success-100 text-success-800' :
              'bg-medical-100 text-medical-800'
            }`}>
              {currentConsultation.status.charAt(0).toUpperCase() + currentConsultation.status.slice(1)}
            </span>
          )}
        </div>
      </div>

      {/* Progress Steps */}
      <div className="card">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
          {['symptoms', 'files', 'analysis'].map((step, index) => (
            <div key={step} className="flex items-center">
              <div className={`flex items-center justify-center w-8 h-8 rounded-full ${
                currentStep === step ? 'bg-primary-600 text-white' :
                index < ['symptoms', 'files', 'analysis'].indexOf(currentStep) ? 'bg-success-500 text-white' :
                'bg-medical-200 text-medical-600'
              }`}>
                {index < ['symptoms', 'files', 'analysis'].indexOf(currentStep) ? (
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <span className="text-sm">{index + 1}</span>
                )}
              </div>
              <span className={`ml-2 text-xs sm:text-sm font-medium truncate ${
                currentStep === step ? 'text-primary-600' : 'text-medical-600'
              }`}>
                {step.charAt(0).toUpperCase() + step.slice(1)}
              </span>
              {index < 2 && (
                <div className={`hidden sm:block w-16 h-0.5 mx-4 ${
                  index < ['symptoms', 'files', 'analysis'].indexOf(currentStep) ? 'bg-success-500' : 'bg-medical-200'
                }`} />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="alert-emergency">
          <p className="text-sm font-medium">{error}</p>
        </div>
      )}

      {/* Step Content */}
      {currentStep === 'symptoms' && (
        <div className="card">
          <h2 className="text-lg sm:text-xl font-semibold text-medical-900 mb-4 sm:mb-6">Describe Your Symptoms</h2>
          
          <form onSubmit={handleSubmit(onSubmitSymptoms)} className="space-y-4 sm:space-y-6">
            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                Chief Complaint *
              </label>
              <textarea
                {...register('chief_complaint', { required: 'Please describe your main concern' })}
                rows={3}
                className="form-input"
                placeholder="Briefly describe your main health concern or reason for this consultation..."
              />
              {errors.chief_complaint && (
                <p className="mt-1 text-sm text-danger-600">{errors.chief_complaint.message}</p>
              )}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
              <div>
                <label className="block text-sm font-medium text-medical-700 mb-2">
                  Location
                </label>
                <input
                  {...register('location')}
                  type="text"
                  className="form-input"
                  placeholder="Where is the symptom located?"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-medical-700 mb-2">
                  Severity (1-10) *
                </label>
                <select
                  {...register('severity', { 
                    required: 'Please rate the severity',
                    valueAsNumber: true
                  })}
                  className="form-input"
                >
                  <option value="">Select severity</option>
                  {[1,2,3,4,5,6,7,8,9,10].map(num => (
                    <option key={num} value={num}>{num} - {num <= 3 ? 'Mild' : num <= 6 ? 'Moderate' : num <= 8 ? 'Severe' : 'Very Severe'}</option>
                  ))}
                </select>
                {errors.severity && (
                  <p className="mt-1 text-sm text-danger-600">{errors.severity.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-medical-700 mb-2">
                  Duration
                </label>
                <input
                  {...register('duration')}
                  type="text"
                  className="form-input"
                  placeholder="How long have you had this symptom?"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-medical-700 mb-2">
                  Onset
                </label>
                <input
                  {...register('onset')}
                  type="text"
                  className="form-input"
                  placeholder="When did it start? How did it begin?"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                Quality/Character
              </label>
              <input
                {...register('quality')}
                type="text"
                className="form-input"
                placeholder="Describe the symptom (sharp, dull, burning, throbbing, etc.)"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">
                Associated Symptoms
              </label>
              <input
                {...register('associated_symptoms')}
                type="text"
                className="form-input"
                placeholder="Other symptoms occurring with this one (separate with commas)"
              />
              <p className="mt-1 text-xs text-medical-500">Example: nausea, dizziness, fatigue</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
              <div>
                <label className="block text-sm font-medium text-medical-700 mb-2">
                  Aggravating Factors
                </label>
                <input
                  {...register('aggravating_factors')}
                  type="text"
                  className="form-input"
                  placeholder="What makes it worse? (separate with commas)"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-medical-700 mb-2">
                  Relieving Factors
                </label>
                <input
                  {...register('relieving_factors')}
                  type="text"
                  className="form-input"
                  placeholder="What makes it better? (separate with commas)"
                />
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 sm:gap-0 sm:justify-end">
              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed w-full sm:w-auto"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <div className="spinner mr-2"></div>
                    Submitting...
                  </div>
                ) : (
                  'Continue to File Upload'
                )}
              </button>
            </div>
          </form>
        </div>
      )}

      {currentStep === 'files' && (
        <div className="card">
          <h2 className="text-lg sm:text-xl font-semibold text-medical-900 mb-4 sm:mb-6">Upload Test Reports & Medical Files</h2>
          
          <div
            {...getRootProps()}
            className={`dropzone ${isDragActive ? 'active' : ''}`}
          >
            <input {...getInputProps()} />
            <div className="text-center">
              <svg className="mx-auto h-12 w-12 text-medical-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              <div className="mt-4">
                <p className="text-lg font-medium text-medical-900">
                  {isDragActive ? 'Drop files here' : 'Upload Medical Files'}
                </p>
                <p className="text-medical-600 mt-2">
                  Drag and drop files here, or <span className="font-medium text-primary-600">browse</span>
                </p>
                <p className="text-sm text-medical-500 mt-1">
                  Supports PDF, JPG, PNG files up to 10MB
                </p>
              </div>
            </div>
          </div>

          {uploadedFiles.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-medium text-medical-900 mb-4">Uploaded Files</h3>
              <div className="space-y-2">
                {uploadedFiles.map((file, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-medical-50 rounded-lg">
                    <div className="flex items-center">
                      <svg className="h-8 w-8 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                      </svg>
                      <div className="ml-3">
                        <p className="text-sm font-medium text-medical-900">{file.name}</p>
                        <p className="text-xs text-medical-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                      </div>
                    </div>
                    <span className="text-success-600 text-sm font-medium">✓ Uploaded</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="flex flex-col sm:flex-row gap-3 sm:gap-0 sm:justify-between mt-6">
            <button
              onClick={() => setCurrentStep('symptoms')}
              className="btn-secondary w-full sm:w-auto"
            >
              Back to Symptoms
            </button>
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed w-full sm:w-auto"
            >
              {isAnalyzing ? (
                <div className="flex items-center">
                  <div className="spinner mr-2"></div>
                  Analyzing...
                </div>
              ) : (
                'Start AI Analysis'
              )}
            </button>
          </div>
        </div>
      )}

      {currentStep === 'analysis' && analysis && (
        <div className="space-y-6">
          <div className="card">
            <h2 className="text-lg sm:text-xl font-semibold text-medical-900 mb-4 sm:mb-6">AI Analysis Results</h2>
            
            <div className={`p-4 rounded-lg border-l-4 mb-6 ${
              analysis.risk_level === 'low' ? 'bg-success-50 border-success-500' :
              analysis.risk_level === 'moderate' ? 'bg-warning-50 border-warning-500' :
              analysis.risk_level === 'high' ? 'bg-danger-50 border-danger-500' :
              'bg-danger-100 border-danger-600'
            }`}>
              <div className="flex items-center mb-2">
                <span className={`severity-indicator ${
                  analysis.risk_level === 'low' ? 'severity-low' :
                  analysis.risk_level === 'moderate' ? 'severity-moderate' :
                  analysis.risk_level === 'high' ? 'severity-high' :
                  'severity-critical'
                }`}></span>
                <h3 className="font-semibold text-lg capitalize">{analysis.risk_level} Risk Level</h3>
              </div>
              <p className="text-sm">{analysis.summary}</p>
            </div>

            {analysis.emergency_alert && (
              <div className="alert-emergency mb-6">
                <h4 className="font-semibold">⚠️ Emergency Alert</h4>
                <p className="mt-1">{analysis.emergency_alert.message}</p>
                {analysis.emergency_alert.immediate_actions?.length > 0 && (
                  <div className="mt-3">
                    <p className="font-medium">Immediate Actions:</p>
                    <ul className="list-disc list-inside mt-1">
                      {analysis.emergency_alert.immediate_actions.map((action, index) => (
                        <li key={index} className="text-sm">{action}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {analysis.key_findings?.length > 0 && (
              <div className="mb-6">
                <h4 className="font-semibold text-medical-900 mb-3">Clinical Assessment</h4>
                <div className="bg-white border border-medical-200 rounded-lg p-4">
                  <ul className="space-y-3">
                    {analysis.key_findings.map((finding, index) => (
                      <li key={index} className="flex items-start">
                        <svg className="h-4 w-4 text-primary-600 mt-1 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                        <span className="text-medical-700 leading-relaxed">{finding}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {analysis.recommendations?.length > 0 && (
              <div className="mb-6">
                <h4 className="font-semibold text-medical-900 mb-3">Recommendations</h4>
                <div className="space-y-4">
                  {analysis.recommendations.map((rec, index) => {
                    // Handle different recommendation formats
                    const recommendation = typeof rec === 'string' ? rec : rec;
                    
                    // Check if it's a structured recommendation object
                    if (typeof recommendation === 'object' && recommendation !== null && 'action' in recommendation) {
                      const structuredRec = recommendation as Recommendation;
                      
                      const categoryIcons: Record<string, string> = {
                        'lifestyle': '🏃‍♂️',
                        'medication': '💊',
                        'follow_up': '📅',
                        'immediate': '⚡',
                        'emergency': '🚨',
                        'urgent': '⏰',
                        'monitoring': '👁️'
                      };
                      
                      const priorityColors: Record<string, string> = {
                        'critical': 'bg-danger-100 border-danger-500 text-danger-800',
                        'high': 'bg-warning-100 border-warning-500 text-warning-800',
                        'medium': 'bg-primary-100 border-primary-500 text-primary-800',
                        'low': 'bg-success-100 border-success-500 text-success-800'
                      };
                      
                      return (
                        <div 
                          key={index} 
                          className={`p-4 rounded-lg border-l-4 ${
                            priorityColors[structuredRec.priority] || 'bg-medical-50 border-medical-300 text-medical-800'
                          }`}
                        >
                          <div className="flex items-start space-x-3">
                            <span className="text-lg">
                              {categoryIcons[structuredRec.category] || '📋'}
                            </span>
                            <div className="flex-1">
                              <div className="flex items-center justify-between mb-2">
                                <span className="text-xs font-medium uppercase tracking-wide opacity-75">
                                  {structuredRec.category?.replace('_', ' ')} • {structuredRec.priority} priority
                                </span>
                                {structuredRec.timeline && (
                                  <span className="text-xs bg-white bg-opacity-50 px-2 py-1 rounded">
                                    {structuredRec.timeline}
                                  </span>
                                )}
                              </div>
                              <p className="text-sm font-medium leading-relaxed">
                                {structuredRec.action}
                              </p>
                            </div>
                          </div>
                        </div>
                      );
                    } else {
                      // Handle simple string recommendations
                      return (
                        <div key={index} className="p-4 bg-medical-50 rounded-lg border-l-4 border-primary-300">
                          <div className="flex items-start space-x-3">
                            <span className="text-lg">📋</span>
                            <p className="text-medical-700 leading-relaxed">
                              {typeof recommendation === 'string' ? recommendation : (recommendation as any).description || (recommendation as any).text || JSON.stringify(recommendation)}
                            </p>
                          </div>
                        </div>
                      );
                    }
                  })}
                </div>
              </div>
            )}

            {analysis.follow_up_suggestions?.length > 0 && (
              <div className="mb-6">
                <h4 className="font-semibold text-medical-900 mb-3">Follow-up Care</h4>
                <div className="bg-success-50 rounded-lg p-4">
                  <div className="flex items-center mb-3">
                    <svg className="h-5 w-5 text-success-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span className="text-sm font-medium text-success-800">Recommended Next Steps</span>
                  </div>
                  <ul className="space-y-3">
                    {analysis.follow_up_suggestions.map((suggestion, index) => (
                      <li key={index} className="flex items-start">
                        <span className="w-2 h-2 bg-success-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                        <span className="text-success-800 leading-relaxed">{suggestion}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            <div className="border-t pt-4">
              <p className="text-sm text-medical-600">
                <strong>Confidence Score:</strong> {analysis.confidence_score}%
              </p>
              <p className="text-xs text-medical-500 mt-2">
                {analysis.disclaimer}
              </p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 sm:gap-0 sm:justify-between">
            <button
              onClick={() => setCurrentStep('files')}
              className="btn-secondary w-full sm:w-auto"
            >
              Back to Files
            </button>
            <button
              onClick={() => navigate('/history')}
              className="btn-primary w-full sm:w-auto"
            >
              View All Consultations
            </button>
          </div>
        </div>
      )}

      {/* Medical Disclaimer */}
      <div className="alert-info">
        <div className="flex">
          <svg className="h-5 w-5 text-primary-600 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
          <div>
            <h4 className="font-medium">Important Medical Disclaimer</h4>
            <p className="mt-1 text-sm">
              This AI analysis is for informational purposes only and should not replace professional medical advice. 
              Always consult with a qualified healthcare provider for medical concerns, especially in emergency situations.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConsultationPage;