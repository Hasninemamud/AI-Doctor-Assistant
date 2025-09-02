import React from 'react';

const ProfilePage: React.FC = () => {
  return (
    <div className="space-y-4 sm:space-y-6">
      <h1 className="text-xl sm:text-2xl font-bold text-medical-900">Profile & Medical History</h1>
      <div className="card">
        <p className="text-sm sm:text-base text-medical-600">
          User profile and medical history management will be implemented here.
        </p>
      </div>
    </div>
  );
};

export default ProfilePage;