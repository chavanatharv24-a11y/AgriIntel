import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Layout = ({ children }) => {
  const location = useLocation();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const isAuthPage = location.pathname === '/' || location.pathname === '/signup';

  if (isAuthPage) {
    return <div className="app-content center-all">{children}</div>;
  }

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

  return (
    <>
      <nav className="navbar">
        <div className="nav-header">
          <Link to="/dashboard" className="nav-brand">AgriIntel</Link>
          <button className="mobile-menu-btn" onClick={toggleSidebar}>
            {isSidebarOpen ? '✕' : '☰'}
          </button>
        </div>
        
        <div className={`nav-links ${isSidebarOpen ? 'open' : ''}`}>
          <Link to="/dashboard" onClick={() => setIsSidebarOpen(false)} className={`nav-item ${location.pathname === '/dashboard' ? 'active' : ''}`}>Dashboard</Link>
          <Link to="/diagnose" onClick={() => setIsSidebarOpen(false)} className={`nav-item ${location.pathname === '/diagnose' ? 'active' : ''}`}>Diagnose</Link>
          <Link to="/market" onClick={() => setIsSidebarOpen(false)} className={`nav-item ${location.pathname === '/market' ? 'active' : ''}`}>Market Prices</Link>
          <Link to="/profile" onClick={() => setIsSidebarOpen(false)} className={`nav-item ${location.pathname === '/profile' ? 'active' : ''}`}>Profile</Link>
          <Link to="/assistant" onClick={() => setIsSidebarOpen(false)} className={`nav-item flex items-center gap-2 ${location.pathname === '/assistant' ? 'active text-emerald-600' : ''}`}>
            🎙️ AI Assistant
          </Link>
        </div>
      </nav>
      {isSidebarOpen && <div className="sidebar-overlay" onClick={toggleSidebar}></div>}
      <div className="app-content">
        {children}
      </div>
    </>
  );
};

export default Layout;
