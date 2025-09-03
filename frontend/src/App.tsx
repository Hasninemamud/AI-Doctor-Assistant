import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

import { RootState } from './store/store';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ConsultationPage from './pages/ConsultationPage';
import EnhancedConsultationPage from './pages/EnhancedConsultationPage';
import HistoryPage from './pages/HistoryPage';
import ProfilePage from './pages/ProfilePage';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';

const App: React.FC = () => {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);

  return (
    <div className="min-h-screen bg-medical-50">
      <Routes>
        {/* Public routes */}
        <Route 
          path="/" 
          element={
            isAuthenticated ? <Navigate to="/app/dashboard" replace /> : <LandingPage />
          } 
        />
        <Route 
          path="/login" 
          element={
            isAuthenticated ? <Navigate to="/app/dashboard" replace /> : <LoginPage />
          } 
        />
        <Route 
          path="/register" 
          element={
            isAuthenticated ? <Navigate to="/app/dashboard" replace /> : <RegisterPage />
          } 
        />
        
        {/* Protected routes */}
        <Route 
          path="/app" 
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/app/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="consultation" element={<ConsultationPage />} />
          <Route path="consultation/:id" element={<ConsultationPage />} />
          <Route path="consultation/enhanced/:id" element={<EnhancedConsultationPage />} />
          <Route path="history" element={<HistoryPage />} />
          <Route path="profile" element={<ProfilePage />} />
        </Route>
        
        {/* Catch all route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
};

export default App;