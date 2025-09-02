import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { User, MedicalHistory } from '../types';
import { userAPI } from '../services/api';

interface UserState {
  profile: User | null;
  medicalHistory: MedicalHistory | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: UserState = {
  profile: null,
  medicalHistory: null,
  isLoading: false,
  error: null,
};

// Async thunks
export const getUserProfile = createAsyncThunk(
  'user/getProfile',
  async (_, { rejectWithValue }) => {
    try {
      const response = await userAPI.getProfile();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to get profile');
    }
  }
);

export const updateUserProfile = createAsyncThunk(
  'user/updateProfile',
  async (profileData: Partial<User>, { rejectWithValue }) => {
    try {
      const response = await userAPI.updateProfile(profileData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to update profile');
    }
  }
);

export const getMedicalHistory = createAsyncThunk(
  'user/getMedicalHistory',
  async (_, { rejectWithValue }) => {
    try {
      const response = await userAPI.getMedicalHistory();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to get medical history');
    }
  }
);

export const updateMedicalHistory = createAsyncThunk(
  'user/updateMedicalHistory',
  async (historyData: Partial<MedicalHistory>, { rejectWithValue }) => {
    try {
      const response = await userAPI.updateMedicalHistory(historyData);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to update medical history');
    }
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // Get profile
    builder
      .addCase(getUserProfile.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(getUserProfile.fulfilled, (state, action) => {
        state.isLoading = false;
        state.profile = action.payload;
      })
      .addCase(getUserProfile.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Update profile
    builder
      .addCase(updateUserProfile.fulfilled, (state, action) => {
        state.profile = action.payload;
      });

    // Get medical history
    builder
      .addCase(getMedicalHistory.fulfilled, (state, action) => {
        state.medicalHistory = action.payload;
      });

    // Update medical history
    builder
      .addCase(updateMedicalHistory.fulfilled, (state, action) => {
        state.medicalHistory = action.payload;
      });
  },
});

export const { clearError } = userSlice.actions;
export default userSlice.reducer;