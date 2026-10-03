import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '../api/client';

const Dashboard = () => {
  const [reading, setReading] = useState(null);
  const [loadingReading, setLoadingReading] = useState(true);
  
  const [recommendation, setRecommendation] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [recError, setRecError] = useState(null);

  const [yieldPrediction, setYieldPrediction] = useState(null);
  const [loadingYield, setLoadingYield] = useState(false);
  const [yieldError, setYieldError] = useState(null);

  const [anomalyResult, setAnomalyResult] = useState(null);
  const [loadingAnomaly, setLoadingAnomaly] = useState(false);
  const [anomalyError, setAnomalyError] = useState(null);

  useEffect(() => {
    const fetchReading = async () => {
      try {
        const response = await apiClient.get('/sensor/readings');
        if (response.data && response.data.length > 0) {
          setReading(response.data[0]);
        }
      } catch (err) {
        console.error("Failed to fetch reading", err);
      } finally {
        setLoadingReading(false);
      }
    };
    fetchReading();
  }, []);

  const handleGetRecommendation = async () => {
    setGenerating(true);
    setRecError(null);
    try {
      const response = await apiClient.post('/recommendations/generate');
      setRecommendation(response.data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setRecError(err.response.data.detail);
      } else {
        setRecError('Failed to generate recommendation.');
      }
    } finally {
      setGenerating(false);
    }
  };

  const handlePredictYield = async () => {
    setLoadingYield(true);
    setYieldError(null);
    try {
      const response = await apiClient.get('/predict/yield');
      setYieldPrediction(response.data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setYieldError(err.response.data.detail);
      } else {
        setYieldError('Failed to generate yield prediction.');
      }
    } finally {
      setLoadingYield(false);
    }
  };

  const handleCheckAnomaly = async () => {
    setLoadingAnomaly(true);
    setAnomalyError(null);
    try {
      const response = await apiClient.get('/predict/anomaly-check');
      setAnomalyResult(response.data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setAnomalyError(err.response.data.detail);
      } else {
        setAnomalyError('Failed to check for anomalies.');
      }
    } finally {
      setLoadingAnomaly(false);
    }
  };

  return (
    <div className="feature-container">
      <div className="dashboard-header">
        <div>
          <h1 className="auth-title" style={{ margin: 0 }}>Farm Dashboard</h1>
          <p className="auth-subtitle">Overview of your farm's health</p>
        </div>
        <Link to="/finance" className="submit-btn" style={{ textDecoration: 'none', width: 'auto', padding: '12px 24px' }}>
          Farm Profitability Calculator
        </Link>
      </div>
      
      <div className="auth-container" style={{ maxWidth: '100%', marginBottom: '30px', animation: 'none', opacity: 1, transform: 'none' }}>
        <div className="dashboard-subheader">
          <h2 style={{ marginTop: 0, marginBottom: 0 }}>Latest Farm Reading</h2>
          <Link to="/log-reading" className="submit-btn" style={{ textDecoration: 'none', width: 'auto', padding: '8px 16px', fontSize: '0.875rem' }}>
            Log New Farm Reading
          </Link>
        </div>
        {loadingReading ? (
          <p style={{ color: 'var(--text-muted)' }}>Loading reading data...</p>
        ) : reading ? (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '20px' }}>
            <div style={{ background: 'var(--bg-dark)', padding: '20px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '8px' }}>Soil Moisture</div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--primary)' }}>{reading.soilMoisture}%</div>
            </div>
            <div style={{ background: 'var(--bg-dark)', padding: '20px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '8px' }}>Temperature</div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--primary)' }}>{reading.temperature}°C</div>
            </div>
            <div style={{ background: 'var(--bg-dark)', padding: '20px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '8px' }}>Humidity</div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--primary)' }}>{reading.humidity}%</div>
            </div>
            <div style={{ background: 'var(--bg-dark)', padding: '20px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '8px' }}>Rain Detected</div>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--primary)' }}>{reading.rainDetected ? 'Yes' : 'No'}</div>
            </div>
          </div>
        ) : (
          <p style={{ color: 'var(--text-muted)' }}>No farm readings logged yet — <Link to="/log-reading" style={{ color: 'var(--primary)', textDecoration: 'none' }}>log your first reading to get started</Link></p>
        )}
      </div>

      <div className="auth-container" style={{ maxWidth: '100%', animation: 'none', opacity: 1, transform: 'none' }}>
        <h2 style={{ marginTop: 0, marginBottom: '20px' }}>AI Agronomist</h2>
        <button 
          onClick={handleGetRecommendation} 
          className="submit-btn" 
          style={{ width: 'auto', padding: '12px 24px' }}
          disabled={generating || !reading}
        >
          {generating ? 'Analyzing data with Gemini...' : 'Get AI Recommendation'}
        </button>
        
        {!reading && <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '10px' }}>Need farm data before generating a recommendation.</p>}
        {recError && <div className="error-message" style={{ marginTop: '20px' }}>{recError}</div>}
        
        {recommendation && (
          <div style={{ marginTop: '30px', background: 'var(--bg-dark)', padding: '24px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
            <div style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Risk Level:</span>
              <span style={{ 
                padding: '6px 14px', 
                borderRadius: '8px', 
                fontWeight: '600',
                fontSize: '0.875rem',
                background: recommendation.riskLevel === 'High' ? 'rgba(239, 68, 68, 0.2)' : recommendation.riskLevel === 'Medium' ? 'rgba(245, 158, 11, 0.2)' : 'rgba(16, 185, 129, 0.2)',
                color: recommendation.riskLevel === 'High' ? '#ef4444' : recommendation.riskLevel === 'Medium' ? '#f59e0b' : '#10b981',
                border: `1px solid ${recommendation.riskLevel === 'High' ? 'rgba(239, 68, 68, 0.5)' : recommendation.riskLevel === 'Medium' ? 'rgba(245, 158, 11, 0.5)' : 'rgba(16, 185, 129, 0.5)'}`
              }}>
                {recommendation.riskLevel}
              </span>
            </div>
            <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6', color: 'var(--text-main)' }}>
              {recommendation.recommendationText}
            </div>
          </div>
        )}
      </div>

      <div className="auth-container" style={{ maxWidth: '100%', animation: 'none', opacity: 1, transform: 'none', marginTop: '30px' }}>
        <h2 style={{ marginTop: 0, marginBottom: '20px' }}>Crop Yield Prediction</h2>
        <button 
          onClick={handlePredictYield} 
          className="submit-btn" 
          style={{ width: 'auto', padding: '12px 24px' }}
          disabled={loadingYield || !reading}
        >
          {loadingYield ? 'Calculating prediction...' : 'Predict Yield'}
        </button>
        
        {!reading && <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '10px' }}>Need farm data before predicting yield.</p>}
        {yieldError && <div className="error-message" style={{ marginTop: '20px' }}>{yieldError}</div>}
        
        {yieldPrediction && (
          <div style={{ marginTop: '30px', background: 'var(--bg-dark)', padding: '24px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '8px' }}>Predicted Yield</div>
            <div style={{ fontSize: '3rem', fontWeight: '700', color: 'var(--primary)', marginBottom: '16px' }}>
              {yieldPrediction.predictedYieldKgPerAcre} <span style={{ fontSize: '1.5rem', color: 'var(--text-muted)', fontWeight: '400' }}>kg/acre</span>
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', margin: 0, lineHeight: '1.5' }}>
              Calculated based on current conditions:<br/>
              Soil Moisture: {yieldPrediction.inputs.soilMoisture}% | Temp: {yieldPrediction.inputs.temperature}°C | Humidity: {yieldPrediction.inputs.humidity}% | Land Size: {yieldPrediction.inputs.landSize} acres | Rain: {yieldPrediction.inputs.rainDetected ? 'Yes' : 'No'}
            </p>
          </div>
        )}
      </div>

      <div className="auth-container" style={{ maxWidth: '100%', animation: 'none', opacity: 1, transform: 'none', marginTop: '30px' }}>
        <h2 style={{ marginTop: 0, marginBottom: '20px' }}>Anomaly Detection</h2>
        <button 
          onClick={handleCheckAnomaly} 
          className="submit-btn" 
          style={{ width: 'auto', padding: '12px 24px' }}
          disabled={loadingAnomaly || !reading}
        >
          {loadingAnomaly ? 'Checking sensor data...' : 'Check for Anomalies'}
        </button>
        
        {!reading && <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '10px' }}>Need farm data before checking for anomalies.</p>}
        {anomalyError && <div className="error-message" style={{ marginTop: '20px' }}>{anomalyError}</div>}
        
        {anomalyResult && (
          <div style={{ marginTop: '30px', background: 'var(--bg-dark)', padding: '24px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
            <div style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Status:</span>
              <span style={{ 
                padding: '6px 14px', 
                borderRadius: '8px', 
                fontWeight: '600',
                fontSize: '0.875rem',
                background: anomalyResult.status === 'Anomalous' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(16, 185, 129, 0.2)',
                color: anomalyResult.status === 'Anomalous' ? '#ef4444' : '#10b981',
                border: `1px solid ${anomalyResult.status === 'Anomalous' ? 'rgba(239, 68, 68, 0.5)' : 'rgba(16, 185, 129, 0.5)'}`
              }}>
                {anomalyResult.status}
              </span>
            </div>
            
            <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '8px' }}>Anomaly Score</div>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--primary)', marginBottom: '16px' }}>
              {anomalyResult.anomalyScore}
            </div>

            <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', margin: 0, lineHeight: '1.5' }}>
              Checked against current conditions:<br/>
              Soil Moisture: {anomalyResult.inputs.soilMoisture}% | Temp: {anomalyResult.inputs.temperature}°C | Humidity: {anomalyResult.inputs.humidity}%
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
