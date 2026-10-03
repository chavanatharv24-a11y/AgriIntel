import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '../api/client';

const Finance = () => {
  const [formData, setFormData] = useState({
    seedCost: 0,
    fertilizerCost: 0,
    laborCost: 0,
    otherCosts: 0,
    sellingPricePerKg: ''
  });
  
  const [financeResult, setFinanceResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setFinanceResult(null);
    
    try {
      const payload = {
        seedCost: parseFloat(formData.seedCost) || 0,
        fertilizerCost: parseFloat(formData.fertilizerCost) || 0,
        laborCost: parseFloat(formData.laborCost) || 0,
        otherCosts: parseFloat(formData.otherCosts) || 0,
        sellingPricePerKg: parseFloat(formData.sellingPricePerKg)
      };
      
      const response = await apiClient.post('/finance/calculate', payload);
      setFinanceResult(response.data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Failed to calculate finances. Ensure you have a farm reading first.');
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
        <h1 className="auth-title" style={{ margin: 0 }}>Farm Profitability Calculator</h1>
        <p className="auth-subtitle">Forecast your costs and margins based on AI yield predictions</p>
      </div>

      <div className="auth-container" style={{ maxWidth: '100%', marginBottom: '30px', animation: 'none', opacity: 1, transform: 'none' }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Seed Cost (₹)</label>
            <input 
              type="number" 
              name="seedCost" 
              value={formData.seedCost} 
              onChange={handleChange} 
              className="auth-input" 
              min="0"
              step="0.01"
            />
          </div>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Fertilizer Cost (₹)</label>
            <input 
              type="number" 
              name="fertilizerCost" 
              value={formData.fertilizerCost} 
              onChange={handleChange} 
              className="auth-input" 
              min="0"
              step="0.01"
            />
          </div>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Labor Cost (₹)</label>
            <input 
              type="number" 
              name="laborCost" 
              value={formData.laborCost} 
              onChange={handleChange} 
              className="auth-input" 
              min="0"
              step="0.01"
            />
          </div>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Other Costs (₹)</label>
            <input 
              type="number" 
              name="otherCosts" 
              value={formData.otherCosts} 
              onChange={handleChange} 
              className="auth-input" 
              min="0"
              step="0.01"
            />
          </div>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Expected Selling Price per Kg (₹) *</label>
            <input 
              type="number" 
              name="sellingPricePerKg" 
              value={formData.sellingPricePerKg} 
              onChange={handleChange} 
              className="auth-input" 
              required
              min="0"
              step="0.01"
            />
          </div>
          
          <button 
            type="submit" 
            className="submit-btn" 
            disabled={loading}
            style={{ marginTop: '10px', width: 'auto', alignSelf: 'flex-start', padding: '12px 24px' }}
          >
            {loading ? 'Calculating...' : 'Calculate Profitability'}
          </button>
        </form>
        
        {error && <div className="error-message" style={{ marginTop: '20px' }}>{error}</div>}
      </div>

      {financeResult && (
        <div className="auth-container" style={{ maxWidth: '100%', animation: 'none', opacity: 1, transform: 'none' }}>
          <h2 style={{ marginTop: 0, marginBottom: '20px' }}>Financial Forecast</h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '20px', marginBottom: '20px' }}>
            <div style={{ background: 'var(--bg-dark)', padding: '20px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '8px' }}>Total Yield</div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: 'var(--primary)' }}>{financeResult.totalYieldKg} kg</div>
            </div>
            
            <div style={{ background: 'var(--bg-dark)', padding: '20px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '8px' }}>Total Cost</div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: 'var(--text-main)' }}>₹{financeResult.totalCost}</div>
            </div>
            
            <div style={{ background: 'var(--bg-dark)', padding: '20px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '8px' }}>Revenue</div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: 'var(--text-main)' }}>₹{financeResult.revenue}</div>
            </div>

            <div style={{ background: 'var(--bg-dark)', padding: '20px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '8px' }}>Profit Margin</div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: 'var(--text-main)' }}>{financeResult.profitMarginPercent}%</div>
            </div>
            
            <div style={{ background: 'var(--bg-dark)', padding: '20px', borderRadius: '16px', border: '1px solid var(--surface-border)' }}>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '8px' }}>Break-Even Price</div>
              <div style={{ fontSize: '1.75rem', fontWeight: '700', color: 'var(--text-main)' }}>₹{financeResult.breakEvenPricePerKg}/kg</div>
            </div>
          </div>
          
          <div style={{ 
            background: financeResult.profit >= 0 ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', 
            padding: '30px', 
            borderRadius: '16px', 
            border: `2px solid ${financeResult.profit >= 0 ? 'rgba(16, 185, 129, 0.5)' : 'rgba(239, 68, 68, 0.5)'}`,
            textAlign: 'center'
          }}>
            <div style={{ color: 'var(--text-muted)', fontSize: '1rem', marginBottom: '10px' }}>Projected Profit</div>
            <div style={{ 
              fontSize: '4rem', 
              fontWeight: '800', 
              color: financeResult.profit >= 0 ? '#10b981' : '#ef4444',
              lineHeight: '1'
            }}>
              ₹{financeResult.profit}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Finance;
