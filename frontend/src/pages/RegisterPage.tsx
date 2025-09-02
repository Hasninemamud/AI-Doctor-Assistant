import React from 'react';

const RegisterPage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-medical-100">
      <div className="max-w-md w-full text-center">
        <h1 className="text-2xl font-bold text-medical-900 mb-4">Register Page</h1>
        <p className="text-medical-600">Registration form will be implemented here</p>
        <a href="/login" className="text-primary-600 hover:text-primary-500 mt-4 inline-block">
          Back to Login
        </a>
      </div>
    </div>
  );
};

export default RegisterPage;