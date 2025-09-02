import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Clock, TrendingUp, AlertTriangle, Activity, Brain, Stethoscope } from 'lucide-react';
import toast from 'react-hot-toast';

import { AppDispatch, RootState } from '../store/store';
import { SymptomTimelineEntry, ComprehensiveAnalysisResponse, TimelinePattern, EmergencyScreeningResult } from '../types';

interface TimelineEntryFormData {
  symptom: string;
  severity: number;
  location: string;
  quality: string;
  duration: string;
  notes: string;
  recorded_at: string;
}

const EnhancedConsultationPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  
  const [currentStep, setCurrentStep] = useState<'timeline' | 'analysis' | 'results'>('timeline');
  const [timelineEntries, setTimelineEntries] = useState<SymptomTimelineEntry[]>([]);
  const [newEntry, setNewEntry] = useState<TimelineEntryFormData>({
    symptom: '',
    severity: 5,
    location: '',
    quality: '',
    duration: '',
    notes: '',
    recorded_at: new Date().toISOString().slice(0, 16)
  });
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResults, setAnalysisResults] = useState<ComprehensiveAnalysisResponse | null>(null);

  const addTimelineEntry = async () => {
    if (!newEntry.symptom) {
      toast.error('Please enter a symptom');
      return;
    }

    try {
      const response = await fetch(`/api/v1/consultations/enhanced/${id}/timeline`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          ...newEntry,
          consultation_id: id
        })
      });

      if (response.ok) {
        const createdEntry = await response.json();
        setTimelineEntries(prev => [...prev, createdEntry]);
        setNewEntry({
          symptom: '',
          severity: 5,
          location: '',
          quality: '',
          duration: '',
          notes: '',
          recorded_at: new Date().toISOString().slice(0, 16)
        });
        toast.success('Timeline entry added');
      }
    } catch (error) {
      toast.error('Failed to add timeline entry');
    }
  };

  const performComprehensiveAnalysis = async () => {
    setIsAnalyzing(true);
    try {
      const response = await fetch(`/api/v1/consultations/enhanced/${id}/analyze/comprehensive`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
          consultation_id: id,
          analysis_types: ['general', 'clinical_analysis'],
          include_emergency_screening: true,
          include_timeline_analysis: true,
          include_test_reports: true,
          include_symptoms: true,
          include_medical_history: true
        })
      });

      if (response.ok) {
        const results = await response.json();
        setAnalysisResults(results);
        setCurrentStep('results');
        toast.success('Comprehensive analysis completed');
      }
    } catch (error) {
      toast.error('Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'moderate': return 'text-yellow-600 bg-yellow-100';
      case 'low': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const renderTimelineStep = () => (
    <div className="space-y-6">
      <div className="card">
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <Clock className="w-5 h-5 mr-2" />
          Symptom Timeline
        </h3>
        
        {/* Add new entry form */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <input
            type="text"
            placeholder="Symptom description"
            value={newEntry.symptom}
            onChange={(e) => setNewEntry(prev => ({...prev, symptom: e.target.value}))}
            className="input"
          />
          <input
            type="datetime-local"
            value={newEntry.recorded_at}
            onChange={(e) => setNewEntry(prev => ({...prev, recorded_at: e.target.value}))}
            className="input"
          />
          <div>
            <label className="block text-sm font-medium mb-1">Severity (1-10)</label>
            <input
              type="range"
              min="1"
              max="10"
              value={newEntry.severity}
              onChange={(e) => setNewEntry(prev => ({...prev, severity: parseInt(e.target.value)}))}
              className="w-full"
            />
            <span className="text-sm text-gray-500">{newEntry.severity}/10</span>
          </div>
          <input
            type="text"
            placeholder="Location"
            value={newEntry.location}
            onChange={(e) => setNewEntry(prev => ({...prev, location: e.target.value}))}
            className="input"
          />
        </div>
        
        <button
          onClick={addTimelineEntry}
          className="btn btn-primary"
        >
          Add Entry
        </button>
      </div>

      {/* Timeline display */}
      <div className="card">
        <h4 className="font-semibold mb-4">Timeline Entries ({timelineEntries.length})</h4>
        <div className="space-y-3">
          {timelineEntries.map((entry, index) => (
            <div key={index} className="flex items-center p-3 bg-gray-50 rounded-lg">
              <div className="flex-1">
                <div className="font-medium">{entry.symptom}</div>
                <div className="text-sm text-gray-600">
                  {new Date(entry.recorded_at).toLocaleString()}
                  {entry.severity && ` • Severity: ${entry.severity}/10`}
                  {entry.location && ` • Location: ${entry.location}`}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <button
        onClick={() => setCurrentStep('analysis')}
        disabled={timelineEntries.length === 0}
        className="btn btn-primary w-full"
      >
        Proceed to Analysis
      </button>
    </div>
  );

  const renderAnalysisStep = () => (
    <div className="space-y-6">
      <div className="card text-center">
        <Brain className="w-16 h-16 mx-auto mb-4 text-blue-600" />
        <h3 className="text-xl font-semibold mb-2">Comprehensive Medical Analysis</h3>
        <p className="text-gray-600 mb-6">
          Our specialized AI models will analyze your symptom timeline, perform emergency screening, 
          and provide comprehensive medical insights.
        </p>
        
        <div className="bg-blue-50 p-4 rounded-lg mb-6">
          <h4 className="font-semibold mb-2">Analysis includes:</h4>
          <ul className="text-sm space-y-1">
            <li>• Emergency condition screening</li>
            <li>• Symptom timeline pattern analysis</li>
            <li>• Clinical differential analysis</li>
            <li>• Risk stratification</li>
            <li>• Specialized medical model insights</li>
          </ul>
        </div>

        <button
          onClick={performComprehensiveAnalysis}
          disabled={isAnalyzing}
          className="btn btn-primary"
        >
          {isAnalyzing ? 'Analyzing...' : 'Start Comprehensive Analysis'}
        </button>
      </div>
    </div>
  );

  const renderResultsStep = () => {
    if (!analysisResults) return null;

    return (
      <div className="space-y-6">
        {/* Emergency Alert */}
        {analysisResults.emergency_screening?.is_emergency && (
          <div className="card border-red-500 bg-red-50">
            <div className="flex items-center mb-4">
              <AlertTriangle className="w-6 h-6 text-red-600 mr-2" />
              <h3 className="text-lg font-semibold text-red-900">Emergency Alert</h3>
            </div>
            <div className="space-y-2">
              {analysisResults.emergency_screening.immediate_actions.map((action, index) => (
                <div key={index} className="text-red-800 font-medium">• {action}</div>
              ))}
            </div>
          </div>
        )}

        {/* Overall Risk Assessment */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Overall Risk Assessment</h3>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskLevelColor(analysisResults.overall_risk_level)}`}>
              {analysisResults.overall_risk_level.toUpperCase()}
            </span>
          </div>
        </div>

        {/* Timeline Analysis */}
        {analysisResults.timeline_analysis && (
          <div className="card">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2" />
              Timeline Analysis
            </h3>
            <p className="text-gray-700 mb-4">{analysisResults.timeline_analysis.timeline_summary}</p>
            
            {analysisResults.timeline_analysis.identified_patterns.length > 0 && (
              <div className="space-y-3">
                <h4 className="font-semibold">Identified Patterns:</h4>
                {analysisResults.timeline_analysis.identified_patterns.map((pattern, index) => (
                  <div key={index} className="bg-blue-50 p-3 rounded-lg">
                    <div className="font-medium">{pattern.pattern_type.replace('_', ' ').toUpperCase()}</div>
                    <div className="text-sm text-gray-600">{pattern.description}</div>
                    <div className="text-sm text-blue-600 mt-1">{pattern.significance}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Recommendations */}
        <div className="card">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Stethoscope className="w-5 h-5 mr-2" />
            Priority Recommendations
          </h3>
          <div className="space-y-3">
            {analysisResults.priority_recommendations.map((rec, index) => (
              <div key={index} className="border-l-4 border-blue-500 pl-4">
                <div className="font-medium">{rec.action}</div>
                <div className="text-sm text-gray-600">
                  Priority: {rec.priority} • Timeline: {rec.timeline}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Enhanced Medical Consultation</h1>
        <div className="flex space-x-2">
          {['timeline', 'analysis', 'results'].map((step, index) => (
            <div
              key={step}
              className={`px-3 py-1 rounded-full text-sm ${
                currentStep === step
                  ? 'bg-blue-600 text-white'
                  : index < ['timeline', 'analysis', 'results'].indexOf(currentStep)
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-200 text-gray-600'
              }`}
            >
              {step.charAt(0).toUpperCase() + step.slice(1)}
            </div>
          ))}
        </div>
      </div>

      {currentStep === 'timeline' && renderTimelineStep()}
      {currentStep === 'analysis' && renderAnalysisStep()}
      {currentStep === 'results' && renderResultsStep()}
    </div>
  );
};

export default EnhancedConsultationPage;