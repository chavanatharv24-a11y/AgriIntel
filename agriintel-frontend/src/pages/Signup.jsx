import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { signup } from '../api/auth';

const Signup = () => {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    email: '',
    password: '',
    cropType: '',
    landSize: ''
  });
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'age' || name === 'landSize' ? (value ? Number(value) : '') : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await signup(formData);
      navigate('/', { state: { message: 'Account created successfully! Please log in.' } });
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Signup failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container" style={{ maxWidth: '420px', padding: '40px' }}>
      <div className="auth-header" style={{ marginBottom: '24px' }}>
        <h1 className="auth-title">AgriIntel</h1>
        <p className="auth-subtitle">Create your farm account</p>
      </div>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="auth-form" style={{ gap: '16px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <div className="input-group">
            <label htmlFor="name">Name</label>
            <input id="name" name="name" type="text" className="input-field" placeholder="Jane Doe" value={formData.name} onChange={handleChange} required disabled={isLoading} />
          </div>
          <div className="input-group">
            <label htmlFor="age">Age</label>
            <input id="age" name="age" type="number" className="input-field" placeholder="30" value={formData.age} onChange={handleChange} required disabled={isLoading} />
          </div>
        </div>
        
        <div className="input-group">
          <label htmlFor="email">Email Address</label>
          <input id="email" name="email" type="email" className="input-field" placeholder="farmer@example.com" value={formData.email} onChange={handleChange} required disabled={isLoading} />
        </div>
        
        <div className="input-group">
          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" className="input-field" placeholder="••••••••" value={formData.password} onChange={handleChange} required disabled={isLoading} />
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <div className="input-group">
            <label htmlFor="cropType">Crop Type</label>
            <input id="cropType" name="cropType" type="text" className="input-field" placeholder="Wheat" value={formData.cropType} onChange={handleChange} disabled={isLoading} />
          </div>
          <div className="input-group">
            <label htmlFor="landSize">Land Size (Acres)</label>
            <input id="landSize" name="landSize" type="number" step="0.1" className="input-field" placeholder="10.5" value={formData.landSize} onChange={handleChange} disabled={isLoading} />
          </div>
        </div>
        
        <button type="submit" className="submit-btn" disabled={isLoading} style={{ marginTop: '16px' }}>
          {isLoading ? 'Creating account...' : 'Sign Up'}
        </button>
      </form>
      
      <p style={{ textAlign: 'center', marginTop: '24px', fontSize: '0.875rem' }}>
        Already have an account? <Link to="/" style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: '600' }}>Sign in</Link>
      </p>
    </div>
  );
};

export default Signup;
