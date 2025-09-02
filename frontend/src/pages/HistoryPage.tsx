import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

import { AppDispatch, RootState } from '../store/store';
import { getConsultations, clearError, setCurrentConsultation } from '../store/consultationSlice';
import { Consultation } from '../types';

const HistoryPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { consultations, isLoading, error } = useSelector(
    (state: RootState) => state.consultation
  );
  
  const [filteredConsultations, setFilteredConsultations] = useState<Consultation[]>([]);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'status'>('newest');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    dispatch(clearError());
    dispatch(getConsultations());
  }, [dispatch]);

  useEffect(() => {
    let filtered = [...consultations];

    // Filter by status
    if (filterStatus !== 'all') {
      filtered = filtered.filter(consultation => consultation.status === filterStatus);
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(consultation => 
        consultation.chief_complaint?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        consultation.id.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Sort consultations
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'newest':
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        case 'oldest':
          return new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
        case 'status':
          return a.status.localeCompare(b.status);
        default:
          return 0;
      }
    });

    setFilteredConsultations(filtered);
  }, [consultations, filterStatus, sortBy, searchTerm]);

  const handleConsultationClick = (consultation: Consultation) => {
    dispatch(setCurrentConsultation(consultation));
    navigate(`/consultation/${consultation.id}`);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft':
        return 'bg-warning-100 text-warning-800';
      case 'active':
        return 'bg-primary-100 text-primary-800';
      case 'completed':
        return 'bg-success-100 text-success-800';
      case 'cancelled':
        return 'bg-danger-100 text-danger-800';
      default:
        return 'bg-medical-100 text-medical-800';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getConsultationSummary = (consultation: Consultation) => {
    if (consultation.chief_complaint && consultation.chief_complaint.length > 100) {
      return consultation.chief_complaint.substring(0, 100) + '...';
    }
    return consultation.chief_complaint || 'No chief complaint recorded';
  };

  if (isLoading && consultations.length === 0) {
    return (
      <div className="space-y-4 sm:space-y-6">
        <h1 className="text-xl sm:text-2xl font-bold text-medical-900">Consultation History</h1>
        <div className="flex justify-center items-center min-h-64">
          <div className="spinner"></div>
          <span className="ml-2 text-sm sm:text-base text-medical-600">Loading consultation history...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-xl sm:text-2xl font-bold text-medical-900">Consultation History</h1>
        <Link
          to="/consultation"
          className="btn-primary w-full sm:w-auto text-center"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          New Consultation
        </Link>
      </div>

      {/* Error Display */}
      {error && (
        <div className="alert-emergency">
          <p className="text-sm font-medium">{error}</p>
        </div>
      )}

      {/* Filters and Search */}
      <div className="card">
        <div className="flex flex-col gap-4">
          {/* Search */}
          <div className="w-full">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-medical-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                type="text"
                className="form-input pl-10"
                placeholder="Search consultations..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
            {/* Status Filter */}
            <div className="flex-1">
              <select
                className="form-input"
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
              >
                <option value="all">All Status</option>
                <option value="draft">Draft</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>

            {/* Sort */}
            <div className="flex-1">
              <select
                className="form-input"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as 'newest' | 'oldest' | 'status')}
              >
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="status">By Status</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div className="ml-2 sm:ml-3 min-w-0">
              <p className="text-xs sm:text-sm font-medium text-medical-600 truncate">Total</p>
              <p className="text-base sm:text-lg font-semibold text-medical-900">{consultations.length}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-success-100 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-success-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
            <div className="ml-2 sm:ml-3 min-w-0">
              <p className="text-xs sm:text-sm font-medium text-medical-600 truncate">Completed</p>
              <p className="text-base sm:text-lg font-semibold text-medical-900">
                {consultations.filter(c => c.status === 'completed').length}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-warning-100 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-warning-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
            <div className="ml-2 sm:ml-3 min-w-0">
              <p className="text-xs sm:text-sm font-medium text-medical-600 truncate">Active</p>
              <p className="text-base sm:text-lg font-semibold text-medical-900">
                {consultations.filter(c => c.status === 'active').length}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-medical-100 rounded-lg flex items-center justify-center">
                <svg className="w-4 h-4 text-medical-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
            <div className="ml-2 sm:ml-3 min-w-0">
              <p className="text-xs sm:text-sm font-medium text-medical-600 truncate">Draft</p>
              <p className="text-base sm:text-lg font-semibold text-medical-900">
                {consultations.filter(c => c.status === 'draft').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Consultations List */}
      {filteredConsultations.length === 0 ? (
        <div className="card text-center py-8 sm:py-12">
          <svg className="mx-auto h-10 w-10 sm:h-12 sm:w-12 text-medical-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 className="text-base sm:text-lg font-medium text-medical-900 mb-2">
            {searchTerm || filterStatus !== 'all' ? 'No consultations found' : 'No consultations yet'}
          </h3>
          <p className="text-sm sm:text-base text-medical-600 mb-4">
            {searchTerm || filterStatus !== 'all' 
              ? 'Try adjusting your search criteria or filters.'
              : 'Start your first consultation to begin tracking your medical consultations.'
            }
          </p>
          {(!searchTerm && filterStatus === 'all') && (
            <Link
              to="/consultation"
              className="btn-primary w-full sm:w-auto"
            >
              Start First Consultation
            </Link>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          {filteredConsultations.map((consultation) => (
            <div
              key={consultation.id}
              className="card hover:shadow-md transition-shadow cursor-pointer"
              onClick={() => handleConsultationClick(consultation)}
            >
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                <div className="flex-1">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-2 sm:mb-2 space-y-2 sm:space-y-0">
                    <div className="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-3">
                      <h3 className="text-base sm:text-lg font-semibold text-medical-900">
                        Consultation #{consultation.id.slice(-8)}
                      </h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium self-start ${getStatusColor(consultation.status)}`}>
                        {consultation.status.charAt(0).toUpperCase() + consultation.status.slice(1)}
                      </span>
                    </div>
                    <div className="text-xs sm:text-sm text-medical-500">
                      {formatDate(consultation.created_at)}
                    </div>
                  </div>
                  
                  <p className="text-sm sm:text-base text-medical-700 mb-3">
                    {getConsultationSummary(consultation)}
                  </p>
                  
                  <div className="flex items-center text-xs sm:text-sm text-medical-500">
                    <svg className="w-3 h-3 sm:w-4 sm:h-4 mr-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span className="truncate">
                      Created {formatDate(consultation.created_at)}
                    </span>
                    {consultation.updated_at && consultation.updated_at !== consultation.created_at && (
                      <>
                        <span className="mx-2 hidden sm:inline">•</span>
                        <span className="hidden sm:inline truncate">Updated {formatDate(consultation.updated_at)}</span>
                      </>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center mt-3 sm:mt-0 sm:ml-4 self-end sm:self-center">
                  <svg className="w-4 h-4 sm:w-5 sm:h-5 text-medical-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Load More (if needed for pagination) */}
      {isLoading && consultations.length > 0 && (
        <div className="flex justify-center py-4">
          <div className="spinner"></div>
          <span className="ml-2 text-sm sm:text-base text-medical-600">Loading more consultations...</span>
        </div>
      )}
    </div>
  );
};

export default HistoryPage;