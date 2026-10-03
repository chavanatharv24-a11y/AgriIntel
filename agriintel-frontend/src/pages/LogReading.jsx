import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import apiClient from '../api/client';

const LogReading = () => {
  const [formData, setFormData] = useState({
    soilMoisture: '',
    temperature: '',
    humidity: '',
    rainDetected: false
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const payload = {
        deviceId: 'manual-entry',
        soilMoisture: parseFloat(formData.soilMoisture) || 0,
        temperature: parseFloat(formData.temperature) || 0,
        humidity: parseFloat(formData.humidity) || 0,
        rainDetected: formData.rainDetected
      };
      
      await apiClient.post('/sensor/readings', payload);
      navigate('/dashboard');
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        const detail = err.response.data.detail;
        setError(Array.isArray(detail) ? 'Please fill all required fields correctly.' : detail);
      } else {
        setError('Failed to log farm reading. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="feature-container">
      <Link to="/dashboard" className="back-link" style={{ display: 'inline-block', marginBottom: '20px', color: 'var(--text-muted)', textDecoration: 'none' }}>
        &larr; Back to Dashboard
      </Link>
      
      <div style={{ marginBottom: '40px' }}>
        <h1 className="auth-title" style={{ margin: 0 }}>Log New Farm Reading</h1>
        <p className="auth-subtitle">Manually input your latest environmental data</p>
      </div>

      <div className="auth-container" style={{ maxWidth: '100%', marginBottom: '30px', animation: 'none', opacity: 1, transform: 'none' }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Soil Moisture (%)</label>
            <input 
              type="number" 
              name="soilMoisture" 
              value={formData.soilMoisture} 
              onChange={handleChange} 
              className="auth-input" 
              min="0"
              max="100"
              step="0.1"
              required
            />
          </div>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Temperature (°C)</label>
            <input 
              type="number" 
              name="temperature" 
              value={formData.temperature} 
              onChange={handleChange} 
              className="auth-input" 
              step="0.1"
              required
            />
          </div>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Humidity (%)</label>
            <input 
              type="number" 
              name="humidity" 
              value={formData.humidity} 
              onChange={handleChange} 
              className="auth-input" 
              min="0"
              max="100"
              step="0.1"
              required
            />
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '10px', marginBottom: '10px' }}>
            <input 
              type="checkbox" 
              name="rainDetected" 
              id="rainDetected"
              checked={formData.rainDetected} 
              onChange={handleChange} 
              style={{ width: '20px', height: '20px', accentColor: 'var(--primary)' }}
            />
            <label htmlFor="rainDetected" style={{ color: 'var(--text-main)', fontSize: '1rem', cursor: 'pointer' }}>Rain Detected</label>
          </div>
          
          <button 
            type="submit" 
            className="submit-btn" 
            disabled={loading}
            style={{ marginTop: '10px', width: 'auto', alignSelf: 'flex-start', padding: '12px 24px' }}
          >
            {loading ? 'Logging Reading...' : 'Submit Reading'}
          </button>
        </form>
        
        {error && <div className="error-message" style={{ marginTop: '20px' }}>{error}</div>}
      </div>
    </div>
  );
};

export default LogReading;
