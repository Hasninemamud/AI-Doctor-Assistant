import React from 'react';
import { Link } from 'react-router-dom';

const DashboardPage: React.FC = () => {
  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <h1 className="text-xl sm:text-2xl font-bold text-medical-900">Dashboard</h1>
        <div className="text-xs sm:text-sm text-medical-600">
          {new Date().toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
          })}
        </div>
      </div>

      {/* Welcome Card */}
      <div className="card bg-gradient-to-r from-primary-500 to-primary-600 text-white">
        <h2 className="text-lg sm:text-xl font-semibold mb-2">Welcome to AI Doctor Assistant</h2>
        <p className="text-primary-100 mb-4 text-sm sm:text-base">
          Get medical analysis and emergency treatment recommendations based on your symptoms and test reports.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
          <Link
            to="/app/consultation"
            className="bg-white text-primary-600 px-4 py-2 rounded-lg font-medium hover:bg-primary-50 transition-colors text-center text-sm sm:text-base"
          >
            Start New Consultation
          </Link>
          <Link
            to="/history"
            className="border border-white text-white px-4 py-2 rounded-lg font-medium hover:bg-white hover:text-primary-600 transition-colors text-center text-sm sm:text-base"
          >
            View History
          </Link>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-success-100 rounded-lg flex-shrink-0">
              <svg className="h-5 w-5 sm:h-6 sm:w-6 text-success-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-3 sm:ml-4 min-w-0 flex-1">
              <p className="text-xs sm:text-sm font-medium text-medical-600 truncate">Total Consultations</p>
              <p className="text-xl sm:text-2xl font-bold text-medical-900">0</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-warning-100 rounded-lg flex-shrink-0">
              <svg className="h-5 w-5 sm:h-6 sm:w-6 text-warning-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-3 sm:ml-4 min-w-0 flex-1">
              <p className="text-xs sm:text-sm font-medium text-medical-600 truncate">Pending Analysis</p>
              <p className="text-xl sm:text-2xl font-bold text-medical-900">0</p>
            </div>
          </div>
        </div>

        <div className="card sm:col-span-2 lg:col-span-1">
          <div className="flex items-center">
            <div className="p-3 bg-primary-100 rounded-lg flex-shrink-0">
              <svg className="h-5 w-5 sm:h-6 sm:w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div className="ml-3 sm:ml-4 min-w-0 flex-1">
              <p className="text-xs sm:text-sm font-medium text-medical-600 truncate">Test Reports</p>
              <p className="text-xl sm:text-2xl font-bold text-medical-900">0</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h3 className="text-base sm:text-lg font-semibold text-medical-900 mb-4">Recent Activity</h3>
        <div className="text-center py-6 sm:py-8">
          <svg className="h-10 w-10 sm:h-12 sm:w-12 text-medical-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p className="text-sm sm:text-base text-medical-600">No recent consultations</p>
          <p className="text-xs sm:text-sm text-medical-500 mt-1">Start your first consultation to see activity here</p>
        </div>
      </div>

      {/* Medical Disclaimer */}
      <div className="alert-info">
        <div className="flex">
          <svg className="h-5 w-5 text-primary-600 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
          <div>
            <h4 className="font-medium">Important Medical Disclaimer</h4>
            <p className="mt-1 text-sm">
              This AI Doctor Assistant is for informational purposes only and should not replace 
              professional medical advice, diagnosis, or treatment. Always seek the advice of your 
              physician or other qualified health provider with any questions you may have regarding 
              a medical condition. In case of emergency, call emergency services immediately.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;