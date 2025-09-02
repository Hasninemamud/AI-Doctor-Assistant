import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../store/authSlice';
import { AppDispatch, RootState } from '../store/store';

interface NavbarProps {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

const Navbar: React.FC<NavbarProps> = ({ sidebarOpen, setSidebarOpen }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <nav className="bg-white shadow-sm border-b border-medical-200 sticky top-0 z-40">
      <div className="px-4 sm:px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            {/* Mobile menu button */}
            <button
              type="button"
              className="lg:hidden -ml-2 mr-3 p-2 rounded-md text-medical-600 hover:text-medical-900 hover:bg-medical-100 transition-colors"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              <span className="sr-only">Open sidebar</span>
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            
            <div className="h-8 w-8 bg-primary-600 rounded-full flex items-center justify-center">
              <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <h1 className="ml-3 text-lg sm:text-xl font-semibold text-medical-900 truncate">
              <span className="hidden sm:inline">AI Doctor Assistant</span>
              <span className="sm:hidden">AI Doctor</span>
            </h1>
          </div>
          
          <div className="flex items-center space-x-2 sm:space-x-4">
            <span className="text-sm text-medical-600 truncate max-w-32 sm:max-w-none">
              <span className="hidden sm:inline">Welcome, </span>{user?.name || 'User'}
            </span>
            <button
              onClick={handleLogout}
              className="text-sm text-danger-600 hover:text-danger-700 font-medium px-2 py-1 rounded hover:bg-danger-50 transition-colors"
            >
              <span className="hidden sm:inline">Logout</span>
              <svg className="sm:hidden h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;