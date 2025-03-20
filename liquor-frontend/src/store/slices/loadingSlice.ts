import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface LoadingState {
  isLoading: boolean;
  loadingText: string;
  loadingCount: number;
  processes: Record<string, boolean>;
}

const initialState: LoadingState = {
  isLoading: false,
  loadingText: '',
  loadingCount: 0,
  processes: {},
};

export const loadingSlice = createSlice({
  name: 'loading',
  initialState,
  reducers: {
    startLoading: (state, action: PayloadAction<string | undefined>) => {
      state.loadingCount += 1;
      state.isLoading = true;
      if (action.payload) {
        state.loadingText = action.payload;
      }
    },
    stopLoading: (state) => {
      state.loadingCount = Math.max(0, state.loadingCount - 1);
      state.isLoading = state.loadingCount > 0;
      if (!state.isLoading) {
        state.loadingText = '';
      }
    },
    startProcess: (state, action: PayloadAction<string>) => {
      state.processes[action.payload] = true;
    },
    stopProcess: (state, action: PayloadAction<string>) => {
      delete state.processes[action.payload];
    },
    resetLoading: (state) => {
      state.isLoading = false;
      state.loadingText = '';
      state.loadingCount = 0;
      state.processes = {};
    },
  },
});

export const { startLoading, stopLoading, startProcess, stopProcess, resetLoading } = loadingSlice.actions;

export default loadingSlice.reducer;