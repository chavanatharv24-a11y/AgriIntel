import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Layout = ({ children }) => {
  const location = useLocation();
  const isAuthPage = location.pathname === '/' || location.pathname === '/signup';

  if (isAuthPage) {
    return <div className="app-content center-all">{children}</div>;
  }

  return (
    <>
      <nav className="navbar">
        <Link to="/dashboard" className="nav-brand">AgriIntel</Link>
        <div className="nav-links">
          <Link to="/dashboard" className={`nav-item ${location.pathname === '/dashboard' ? 'active' : ''}`}>Dashboard</Link>
          <Link to="/diagnose" className={`nav-item ${location.pathname === '/diagnose' ? 'active' : ''}`}>Diagnose</Link>
          <Link to="/market" className={`nav-item ${location.pathname === '/market' ? 'active' : ''}`}>Market Prices</Link>
          <Link to="/profile" className={`nav-item ${location.pathname === '/profile' ? 'active' : ''}`}>Profile</Link>

          <Link to="/assistant" className={`nav-item flex items-center gap-2 ${location.pathname === '/assistant' ? 'active text-emerald-600' : ''}`}>
            🎙️ AI Assistant
          </Link>
        </div>
      </nav>
      <div className="app-content">
        {children}
      </div>
    </>
  );
};

export default Layout;
