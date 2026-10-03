import React, { useState } from 'react';
import apiClient from '../api/client';
import { Link } from 'react-router-dom';

const Diagnose = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [recommendation, setRecommendation] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      // Clear previous results
      setRecommendation(null);
      setError(null);
    }
  };

  const handleDiagnose = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    setRecommendation(null);

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await apiClient.post('/recommendations/diagnose', formData);
      setRecommendation(response.data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Failed to diagnose image.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="feature-container">
      <div style={{ marginBottom: '40px' }}>
        <h1 className="auth-title" style={{ margin: 0 }}>Crop Disease Diagnosis</h1>
        <p className="auth-subtitle">Upload a photo to get AI recommendations</p>
      </div>

      <div className="auth-container" style={{ maxWidth: '100%', animation: 'none', opacity: 1, transform: 'none' }}>
        <h2 style={{ marginTop: 0, marginBottom: '20px' }}>Upload or Take a Photo</h2>
        
        <div style={{ marginBottom: '20px' }}>
          <input 
            type="file" 
            accept="image/*" 
            capture="environment" 
            onChange={handleFileChange}
            style={{ display: 'block', marginBottom: '20px' }}
          />
        </div>

        {previewUrl && (
          <div style={{ marginBottom: '20px' }}>
            <img 
              src={previewUrl} 
              alt="Preview" 
              style={{ maxWidth: '100%', maxHeight: '400px', borderRadius: '16px', border: '1px solid var(--surface-border)' }} 
            />
          </div>
        )}

        <button 
          onClick={handleDiagnose} 
          className="submit-btn" 
          style={{ width: 'auto', padding: '12px 24px' }}
          disabled={loading || !selectedFile}
        >
          {loading ? 'Analyzing image...' : 'Diagnose'}
        </button>

        {error && <div className="error-message" style={{ marginTop: '20px' }}>{error}</div>}

        {recommendation && (
          <div style={{ marginTop: '30px', background: 'var(--bg-dark)', padding: '24px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
            <div style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Disease Name:</span>
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
    </div>
  );
};

export default Diagnose;
