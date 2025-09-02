import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import consultationReducer from './consultationSlice';
import userReducer from './userSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    consultation: consultationReducer,
    user: userReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;