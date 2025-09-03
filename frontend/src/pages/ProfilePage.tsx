import React, { useState, useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../store/store';
import { getUserProfile, updateUserProfile, getMedicalHistory, updateMedicalHistory, clearError } from '../store/userSlice';
import { User, MedicalHistory } from '../types';

const ProfilePage: React.FC = () => {
  const dispatch = useAppDispatch();
  const { profile, medicalHistory, isLoading, error } = useAppSelector((state) => state.user);
  const { user } = useAppSelector((state) => state.auth);

  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [isEditingMedical, setIsEditingMedical] = useState(false);
  const [profileForm, setProfileForm] = useState<Partial<User>>({});
  const [medicalForm, setMedicalForm] = useState<Partial<MedicalHistory>>({});
  const [newAllergy, setNewAllergy] = useState('');
  const [newMedication, setNewMedication] = useState('');
  const [newCondition, setNewCondition] = useState('');
  const [newFamilyHistory, setNewFamilyHistory] = useState('');

  useEffect(() => {
    dispatch(getUserProfile());
    dispatch(getMedicalHistory());
  }, [dispatch]);

  useEffect(() => {
    if (profile) {
      setProfileForm({
        name: profile.name,
        email: profile.email,
        phone: profile.phone || '',
        date_of_birth: profile.date_of_birth || '',
        gender: profile.gender || 'other',
      });
    }
  }, [profile]);

  useEffect(() => {
    if (medicalHistory) {
      setMedicalForm({
        allergies: medicalHistory.allergies || [],
        medications: medicalHistory.medications || [],
        conditions: medicalHistory.conditions || [],
        family_history: medicalHistory.family_history || [],
      });
    }
  }, [medicalHistory]);

  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dispatch(updateUserProfile(profileForm)).unwrap();
      setIsEditingProfile(false);
    } catch (error) {
      console.error('Failed to update profile:', error);
    }
  };

  const handleMedicalSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dispatch(updateMedicalHistory(medicalForm)).unwrap();
      setIsEditingMedical(false);
    } catch (error) {
      console.error('Failed to update medical history:', error);
    }
  };

  const addToArray = (field: keyof MedicalHistory, value: string, setter: React.Dispatch<React.SetStateAction<string>>) => {
    if (value.trim()) {
      const currentArray = medicalForm[field] as string[] || [];
      setMedicalForm(prev => ({
        ...prev,
        [field]: [...currentArray, value.trim()]
      }));
      setter('');
    }
  };

  const removeFromArray = (field: keyof MedicalHistory, index: number) => {
    const currentArray = medicalForm[field] as string[] || [];
    setMedicalForm(prev => ({
      ...prev,
      [field]: currentArray.filter((_, i) => i !== index)
    }));
  };

  const clearErrorMessage = () => {
    dispatch(clearError());
  };

  if (isLoading && !profile) {
    return (
      <div className="space-y-4 sm:space-y-6">
        <h1 className="text-xl sm:text-2xl font-bold text-medical-900">Profile & Medical History</h1>
        <div className="card text-center py-8">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-medical-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      <h1 className="text-xl sm:text-2xl font-bold text-medical-900">Profile & Medical History</h1>
      
      {error && (
        <div className="alert-warning">
          <div className="flex justify-between items-start">
            <p>{error}</p>
            <button 
              onClick={clearErrorMessage}
              className="text-warning-700 hover:text-warning-800 ml-2"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* Profile Information */}
      <div className="card">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
          <h2 className="text-lg sm:text-xl font-semibold text-medical-900 mb-2 sm:mb-0">Personal Information</h2>
          <button
            onClick={() => setIsEditingProfile(!isEditingProfile)}
            className="btn-secondary text-sm"
          >
            {isEditingProfile ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>

        {isEditingProfile ? (
          <form onSubmit={handleProfileSubmit} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-medical-700 mb-1">Full Name</label>
                <input
                  type="text"
                  value={profileForm.name || ''}
                  onChange={(e) => setProfileForm(prev => ({ ...prev, name: e.target.value }))}
                  className="form-input"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-medical-700 mb-1">Email</label>
                <input
                  type="email"
                  value={profileForm.email || ''}
                  onChange={(e) => setProfileForm(prev => ({ ...prev, email: e.target.value }))}
                  className="form-input"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-medical-700 mb-1">Phone Number</label>
                <input
                  type="tel"
                  value={profileForm.phone || ''}
                  onChange={(e) => setProfileForm(prev => ({ ...prev, phone: e.target.value }))}
                  className="form-input"
                  placeholder="+1 (555) 123-4567"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-medical-700 mb-1">Date of Birth</label>
                <input
                  type="date"
                  value={profileForm.date_of_birth || ''}
                  onChange={(e) => setProfileForm(prev => ({ ...prev, date_of_birth: e.target.value }))}
                  className="form-input"
                />
              </div>
              <div className="sm:col-span-2">
                <label className="block text-sm font-medium text-medical-700 mb-1">Gender</label>
                <select
                  value={profileForm.gender || 'other'}
                  onChange={(e) => setProfileForm(prev => ({ ...prev, gender: e.target.value as 'male' | 'female' | 'other' }))}
                  className="form-input"
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other/Prefer not to say</option>
                </select>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 pt-4">
              <button type="submit" className="btn-primary" disabled={isLoading}>
                {isLoading ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                type="button"
                onClick={() => setIsEditingProfile(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div className="space-y-3">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium text-medical-600">Full Name</p>
                <p className="text-medical-900">{profile?.name || 'Not provided'}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-medical-600">Email</p>
                <p className="text-medical-900">{profile?.email || 'Not provided'}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-medical-600">Phone Number</p>
                <p className="text-medical-900">{profile?.phone || 'Not provided'}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-medical-600">Date of Birth</p>
                <p className="text-medical-900">
                  {profile?.date_of_birth 
                    ? new Date(profile.date_of_birth).toLocaleDateString() 
                    : 'Not provided'
                  }
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-medical-600">Gender</p>
                <p className="text-medical-900 capitalize">
                  {profile?.gender === 'other' ? 'Other/Prefer not to say' : profile?.gender || 'Not provided'}
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-medical-600">Account Status</p>
                <div className="flex items-center space-x-2">
                  <span className={`inline-block w-2 h-2 rounded-full ${
                    profile?.is_verified ? 'bg-success-500' : 'bg-warning-500'
                  }`}></span>
                  <p className="text-medical-900">
                    {profile?.is_verified ? 'Verified' : 'Unverified'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Medical History */}
      <div className="card">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
          <h2 className="text-lg sm:text-xl font-semibold text-medical-900 mb-2 sm:mb-0">Medical History</h2>
          <button
            onClick={() => setIsEditingMedical(!isEditingMedical)}
            className="btn-secondary text-sm"
          >
            {isEditingMedical ? 'Cancel' : 'Edit Medical History'}
          </button>
        </div>

        {isEditingMedical ? (
          <form onSubmit={handleMedicalSubmit} className="space-y-6">
            {/* Allergies */}
            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">Allergies</label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={newAllergy}
                  onChange={(e) => setNewAllergy(e.target.value)}
                  placeholder="Add allergy"
                  className="form-input flex-1"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      addToArray('allergies', newAllergy, setNewAllergy);
                    }
                  }}
                />
                <button
                  type="button"
                  onClick={() => addToArray('allergies', newAllergy, setNewAllergy)}
                  className="btn-secondary px-3"
                >
                  Add
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {(medicalForm.allergies || []).map((allergy, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-danger-100 text-danger-800"
                  >
                    {allergy}
                    <button
                      type="button"
                      onClick={() => removeFromArray('allergies', index)}
                      className="ml-2 text-danger-600 hover:text-danger-800"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {/* Current Medications */}
            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">Current Medications</label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={newMedication}
                  onChange={(e) => setNewMedication(e.target.value)}
                  placeholder="Add medication"
                  className="form-input flex-1"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      addToArray('medications', newMedication, setNewMedication);
                    }
                  }}
                />
                <button
                  type="button"
                  onClick={() => addToArray('medications', newMedication, setNewMedication)}
                  className="btn-secondary px-3"
                >
                  Add
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {(medicalForm.medications || []).map((medication, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary-100 text-primary-800"
                  >
                    {medication}
                    <button
                      type="button"
                      onClick={() => removeFromArray('medications', index)}
                      className="ml-2 text-primary-600 hover:text-primary-800"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {/* Medical Conditions */}
            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">Medical Conditions</label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={newCondition}
                  onChange={(e) => setNewCondition(e.target.value)}
                  placeholder="Add medical condition"
                  className="form-input flex-1"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      addToArray('conditions', newCondition, setNewCondition);
                    }
                  }}
                />
                <button
                  type="button"
                  onClick={() => addToArray('conditions', newCondition, setNewCondition)}
                  className="btn-secondary px-3"
                >
                  Add
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {(medicalForm.conditions || []).map((condition, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-warning-100 text-warning-800"
                  >
                    {condition}
                    <button
                      type="button"
                      onClick={() => removeFromArray('conditions', index)}
                      className="ml-2 text-warning-600 hover:text-warning-800"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {/* Family History */}
            <div>
              <label className="block text-sm font-medium text-medical-700 mb-2">Family Medical History</label>
              <div className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={newFamilyHistory}
                  onChange={(e) => setNewFamilyHistory(e.target.value)}
                  placeholder="Add family medical history"
                  className="form-input flex-1"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      addToArray('family_history', newFamilyHistory, setNewFamilyHistory);
                    }
                  }}
                />
                <button
                  type="button"
                  onClick={() => addToArray('family_history', newFamilyHistory, setNewFamilyHistory)}
                  className="btn-secondary px-3"
                >
                  Add
                </button>
              </div>
              <div className="flex flex-wrap gap-2">
                {(medicalForm.family_history || []).map((history, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-medical-200 text-medical-800"
                  >
                    {history}
                    <button
                      type="button"
                      onClick={() => removeFromArray('family_history', index)}
                      className="ml-2 text-medical-600 hover:text-medical-800"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 pt-4">
              <button type="submit" className="btn-primary" disabled={isLoading}>
                {isLoading ? 'Saving...' : 'Save Medical History'}
              </button>
              <button
                type="button"
                onClick={() => setIsEditingMedical(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div className="space-y-4">
            {/* Display Medical History */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <h4 className="font-medium text-medical-700 mb-2">Allergies</h4>
                {medicalHistory?.allergies && medicalHistory.allergies.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {medicalHistory.allergies.map((allergy, index) => (
                      <span key={index} className="px-3 py-1 rounded-full text-sm bg-danger-100 text-danger-800">
                        {allergy}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-medical-600">No allergies recorded</p>
                )}
              </div>

              <div>
                <h4 className="font-medium text-medical-700 mb-2">Current Medications</h4>
                {medicalHistory?.medications && medicalHistory.medications.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {medicalHistory.medications.map((medication, index) => (
                      <span key={index} className="px-3 py-1 rounded-full text-sm bg-primary-100 text-primary-800">
                        {typeof medication === 'string' ? medication : medication.name || 'Unknown'}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-medical-600">No medications recorded</p>
                )}
              </div>

              <div>
                <h4 className="font-medium text-medical-700 mb-2">Medical Conditions</h4>
                {medicalHistory?.conditions && medicalHistory.conditions.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {medicalHistory.conditions.map((condition, index) => (
                      <span key={index} className="px-3 py-1 rounded-full text-sm bg-warning-100 text-warning-800">
                        {condition}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-medical-600">No conditions recorded</p>
                )}
              </div>

              <div>
                <h4 className="font-medium text-medical-700 mb-2">Family Medical History</h4>
                {medicalHistory?.family_history && medicalHistory.family_history.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {medicalHistory.family_history.map((history, index) => (
                      <span key={index} className="px-3 py-1 rounded-full text-sm bg-medical-200 text-medical-800">
                        {history}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-medical-600">No family history recorded</p>
                )}
              </div>
            </div>

            {(!medicalHistory?.allergies?.length && 
              !medicalHistory?.medications?.length && 
              !medicalHistory?.conditions?.length && 
              !medicalHistory?.family_history?.length) && (
              <div className="text-center py-6">
                <svg className="h-12 w-12 text-medical-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p className="text-medical-600 mb-2">No medical history recorded</p>
                <p className="text-sm text-medical-500">Click "Edit Medical History" to add your medical information</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Medical Disclaimer */}
      <div className="alert-info">
        <div className="flex">
          <svg className="h-5 w-5 text-primary-600 mr-2 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
          <div>
            <h4 className="font-medium">Privacy & Security</h4>
            <p className="mt-1 text-sm">
              Your medical information is encrypted and secure. This information helps provide 
              more accurate medical analysis and recommendations. Only you and authorized healthcare 
              providers can access this information.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;