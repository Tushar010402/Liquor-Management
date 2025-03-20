import React, { useEffect } from 'react';
import { BrowserRouter as Router, useRoutes } from 'react-router-dom';
import { CssBaseline } from '@mui/material';
import { Provider } from 'react-redux';
import ThemeProvider from './theme/ThemeProvider';
import AuthProvider from './contexts/AuthContext';
import { store, useAppDispatch } from './store';
import { loadPreferencesFromStorage } from './store/slices/userPreferencesSlice';
import routes from './routes';
import Notifications from './components/common/Notifications';
import GlobalLoader from './components/common/GlobalLoader';

// App Router component that uses the routes configuration
const AppRouter = () => {
  const routeElements = useRoutes(routes);
  return routeElements;
};

// App Content component that has access to Redux store
const AppContent = () => {
  const dispatch = useAppDispatch();

  // Load user preferences from localStorage on app start
  useEffect(() => {
    dispatch(loadPreferencesFromStorage());
  }, [dispatch]);

  return (
    <Router>
      <AuthProvider>
        <CssBaseline />
        <GlobalLoader />
        <Notifications />
        <AppRouter />
      </AuthProvider>
    </Router>
  );
};

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <ThemeProvider>
        <AppContent />
      </ThemeProvider>
    </Provider>
  );
};

export default App;
