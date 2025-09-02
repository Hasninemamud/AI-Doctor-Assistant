import React from 'react';

const HistoryPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-medical-900">Consultation History</h1>
      <div className="card">
        <p className="text-medical-600">
          Consultation history and past analyses will be displayed here.
        </p>
      </div>
    </div>
  );
};

export default HistoryPage;