import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Consultation, AnalysisResponse, TestReport } from '../types';
import { consultationAPI } from '../services/api';

interface ConsultationState {
  currentConsultation: Consultation | null;
  consultations: Consultation[];
  analysis: AnalysisResponse | null;
  testReports: TestReport[];
  isLoading: boolean;
  isAnalyzing: boolean;
  error: string | null;
}

const initialState: ConsultationState = {
  currentConsultation: null,
  consultations: [],
  analysis: null,
  testReports: [],
  isLoading: false,
  isAnalyzing: false,
  error: null,
};

// Async thunks
export const createConsultation = createAsyncThunk(
  'consultation/create',
  async (_, { rejectWithValue }) => {
    try {
      const response = await consultationAPI.create({});
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to create consultation');
    }
  }
);

export const getConsultations = createAsyncThunk(
  'consultation/getAll',
  async (_, { rejectWithValue }) => {
    try {
      const response = await consultationAPI.getAll();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to get consultations');
    }
  }
);

export const getConsultation = createAsyncThunk(
  'consultation/getOne',
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await consultationAPI.getById(id);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to get consultation');
    }
  }
);

export const submitSymptoms = createAsyncThunk(
  'consultation/submitSymptoms',
  async ({ id, symptoms }: { id: string; symptoms: any }, { rejectWithValue }) => {
    try {
      const response = await consultationAPI.submitSymptoms(id, symptoms);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to submit symptoms');
    }
  }
);

export const analyzeConsultation = createAsyncThunk(
  'consultation/analyze',
  async (consultationId: string, { rejectWithValue }) => {
    try {
      const response = await consultationAPI.analyze(consultationId);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Analysis failed');
    }
  }
);

export const uploadTestReport = createAsyncThunk(
  'consultation/uploadTestReport',
  async ({ consultationId, file }: { consultationId: string; file: File }, { rejectWithValue }) => {
    try {
      const response = await consultationAPI.uploadFile(consultationId, file);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'File upload failed');
    }
  }
);

const consultationSlice = createSlice({
  name: 'consultation',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearAnalysis: (state) => {
      state.analysis = null;
    },
    setCurrentConsultation: (state, action: PayloadAction<Consultation | null>) => {
      state.currentConsultation = action.payload;
    },
  },
  extraReducers: (builder) => {
    // Create consultation
    builder
      .addCase(createConsultation.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createConsultation.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentConsultation = action.payload;
        state.consultations.unshift(action.payload);
      })
      .addCase(createConsultation.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Get consultations
    builder
      .addCase(getConsultations.fulfilled, (state, action) => {
        state.consultations = action.payload;
      });

    // Get consultation
    builder
      .addCase(getConsultation.fulfilled, (state, action) => {
        state.currentConsultation = action.payload;
      });

    // Submit symptoms
    builder
      .addCase(submitSymptoms.fulfilled, (state, action) => {
        state.currentConsultation = action.payload;
      });

    // Analyze consultation
    builder
      .addCase(analyzeConsultation.pending, (state) => {
        state.isAnalyzing = true;
        state.error = null;
      })
      .addCase(analyzeConsultation.fulfilled, (state, action) => {
        state.isAnalyzing = false;
        state.analysis = action.payload;
      })
      .addCase(analyzeConsultation.rejected, (state, action) => {
        state.isAnalyzing = false;
        state.error = action.payload as string;
      });

    // Upload test report
    builder
      .addCase(uploadTestReport.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(uploadTestReport.fulfilled, (state, action) => {
        state.isLoading = false;
        // Add uploaded file to test reports if needed
      })
      .addCase(uploadTestReport.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, clearAnalysis, setCurrentConsultation } = consultationSlice.actions;
export default consultationSlice.reducer;