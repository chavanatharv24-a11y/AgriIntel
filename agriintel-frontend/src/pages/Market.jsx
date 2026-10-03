import React, { useState, useEffect } from 'react';

const MOCK_MARKET_DATA = [
  { id: 1, crop: 'Wheat (Sharbati)', location: 'Pune APMC', price: '₹3,200', change: '+2.5%' },
  { id: 2, crop: 'Cotton (Long Staple)', location: 'Nagpur APMC', price: '₹7,500', change: '-1.2%' },
  { id: 3, crop: 'Soyabean (Yellow)', location: 'Latur APMC', price: '₹4,800', change: '+0.8%' },
  { id: 4, crop: 'Onion (Red)', location: 'Nashik APMC', price: '₹2,400', change: '+5.4%' },
  { id: 5, crop: 'Sugarcane', location: 'Kolhapur APMC', price: '₹3,150', change: '0.0%' },
  { id: 6, crop: 'Rice (Basmati)', location: 'Gondia APMC', price: '₹5,600', change: '+1.5%' },
];

const Market = () => {
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API fetch delay
    const timer = setTimeout(() => {
      setPrices(MOCK_MARKET_DATA);
      setLoading(false);
    }, 800);
    
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="feature-container">
      <div style={{ marginBottom: '32px' }}>
        <h1 className="auth-title" style={{ margin: '0 0 8px 0' }}>Market Prices</h1>
        <p className="auth-subtitle">Live mandi rates across Maharashtra APMCs</p>
      </div>

      {loading ? (
        <div style={{ color: 'var(--text-muted)', fontSize: '1.2rem' }}>Fetching live prices...</div>
      ) : (
        <div className="market-grid">
          {prices.map((item) => (
            <div key={item.id} className="market-card">
              <div className="market-crop-name">{item.crop}</div>
              <div className="market-location">📍 {item.location}</div>
              
              <div className="market-price-box">
                <div>
                  <span className="market-price">{item.price}</span>
                  <span className="market-unit"> / Quintal</span>
                </div>
                <div style={{ 
                  color: item.change.startsWith('+') ? '#10b981' : item.change.startsWith('-') ? '#ef4444' : '#94a3b8',
                  fontWeight: '600',
                  background: item.change.startsWith('+') ? 'rgba(16, 185, 129, 0.15)' : item.change.startsWith('-') ? 'rgba(239, 68, 68, 0.15)' : 'rgba(148, 163, 184, 0.15)',
                  padding: '4px 10px',
                  borderRadius: '20px',
                  fontSize: '0.85rem'
                }}>
                  {item.change}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Market;
