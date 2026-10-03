import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { login } from '../api/auth';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const successMessage = location.state?.message;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Login failed. Please check your credentials.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-header">
        <h1 className="auth-title">AgriIntel</h1>
        <p className="auth-subtitle">Sign in to your farm dashboard</p>
      </div>
      
      {successMessage && <div style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.2)', color: 'var(--primary)', padding: '12px', borderRadius: '12px', fontSize: '0.875rem', textAlign: 'center', marginBottom: '20px' }}>{successMessage}</div>}
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="auth-form">
        <div className="input-group">
          <label htmlFor="email">Email Address</label>
          <input 
            id="email"
            type="email" 
            className="input-field"
            placeholder="farmer@example.com" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
            disabled={isLoading}
          />
        </div>
        
        <div className="input-group">
          <label htmlFor="password">Password</label>
          <input 
            id="password"
            type="password" 
            className="input-field"
            placeholder="••••••••" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
            disabled={isLoading}
          />
        </div>
        
        <button type="submit" className="submit-btn" disabled={isLoading}>
          {isLoading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>
      
      <p style={{ textAlign: 'center', marginTop: '24px', fontSize: '0.875rem' }}>
        Don't have an account? <Link to="/signup" style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: '600' }}>Sign up</Link>
      </p>
    </div>
  );
};

export default Login;
