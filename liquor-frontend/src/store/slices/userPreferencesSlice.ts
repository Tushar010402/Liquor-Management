import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export type ThemeMode = 'light' | 'dark' | 'system';

interface UserPreferencesState {
  themeMode: ThemeMode;
  sidebarCollapsed: boolean;
  tablePageSize: number;
  dateFormat: string;
  timeFormat: string;
  currency: string;
  language: string;
}

const initialState: UserPreferencesState = {
  themeMode: 'light',
  sidebarCollapsed: false,
  tablePageSize: 10,
  dateFormat: 'MM/dd/yyyy',
  timeFormat: 'hh:mm a',
  currency: 'INR',
  language: 'en',
};

export const userPreferencesSlice = createSlice({
  name: 'userPreferences',
  initialState,
  reducers: {
    setThemeMode: (state, action: PayloadAction<ThemeMode>) => {
      state.themeMode = action.payload;
      localStorage.setItem('themeMode', action.payload);
    },
    toggleSidebar: (state) => {
      state.sidebarCollapsed = !state.sidebarCollapsed;
      localStorage.setItem('sidebarCollapsed', String(state.sidebarCollapsed));
    },
    setSidebarCollapsed: (state, action: PayloadAction<boolean>) => {
      state.sidebarCollapsed = action.payload;
      localStorage.setItem('sidebarCollapsed', String(action.payload));
    },
    setTablePageSize: (state, action: PayloadAction<number>) => {
      state.tablePageSize = action.payload;
      localStorage.setItem('tablePageSize', String(action.payload));
    },
    setDateFormat: (state, action: PayloadAction<string>) => {
      state.dateFormat = action.payload;
      localStorage.setItem('dateFormat', action.payload);
    },
    setTimeFormat: (state, action: PayloadAction<string>) => {
      state.timeFormat = action.payload;
      localStorage.setItem('timeFormat', action.payload);
    },
    setCurrency: (state, action: PayloadAction<string>) => {
      state.currency = action.payload;
      localStorage.setItem('currency', action.payload);
    },
    setLanguage: (state, action: PayloadAction<string>) => {
      state.language = action.payload;
      localStorage.setItem('language', action.payload);
    },
    loadPreferencesFromStorage: (state) => {
      // Load preferences from localStorage if available
      const themeMode = localStorage.getItem('themeMode') as ThemeMode | null;
      const sidebarCollapsed = localStorage.getItem('sidebarCollapsed');
      const tablePageSize = localStorage.getItem('tablePageSize');
      const dateFormat = localStorage.getItem('dateFormat');
      const timeFormat = localStorage.getItem('timeFormat');
      const currency = localStorage.getItem('currency');
      const language = localStorage.getItem('language');

      if (themeMode) state.themeMode = themeMode;
      if (sidebarCollapsed) state.sidebarCollapsed = sidebarCollapsed === 'true';
      if (tablePageSize) state.tablePageSize = parseInt(tablePageSize, 10);
      if (dateFormat) state.dateFormat = dateFormat;
      if (timeFormat) state.timeFormat = timeFormat;
      if (currency) state.currency = currency;
      if (language) state.language = language;
    },
  },
});

export const {
  setThemeMode,
  toggleSidebar,
  setSidebarCollapsed,
  setTablePageSize,
  setDateFormat,
  setTimeFormat,
  setCurrency,
  setLanguage,
  loadPreferencesFromStorage,
} = userPreferencesSlice.actions;

export default userPreferencesSlice.reducer;