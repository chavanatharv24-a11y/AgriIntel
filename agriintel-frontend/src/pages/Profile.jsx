import React, { useEffect, useState, useRef } from 'react';
import apiClient from '../api/client';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState(null);
  
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    cropType: '',
    landSize: ''
  });
  
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await apiClient.get('/users/me');
      setProfile(response.data);
      setFormData({
        name: response.data.name || '',
        age: response.data.age || '',
        cropType: response.data.cropType || '',
        landSize: response.data.landSize || ''
      });
    } catch (err) {
      setError('Failed to load profile.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setUpdating(true);
    setError(null);
    setSuccessMsg(null);
    
    try {
      const payload = {
        name: formData.name,
        age: parseInt(formData.age) || 0,
        cropType: formData.cropType,
        landSize: parseFloat(formData.landSize) || 0
      };
      
      const response = await apiClient.put('/users/me', payload);
      setProfile(response.data);
      setSuccessMsg('Profile updated successfully!');
    } catch (err) {
      setError('Failed to update profile.');
    } finally {
      setUpdating(false);
    }
  };

  const handlePhotoUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await apiClient.post('/users/me/photo', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setProfile(prev => ({ ...prev, photoUrl: response.data.photoUrl }));
      setSuccessMsg('Photo updated successfully!');
    } catch (err) {
      setError('Failed to upload photo.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  if (loading) {
    return <div className="feature-container"><p>Loading profile...</p></div>;
  }

  return (
    <div className="feature-container">
      <div style={{ marginBottom: '40px' }}>
        <h1 className="auth-title" style={{ margin: 0 }}>Farmer Profile</h1>
        <p className="auth-subtitle">Manage your personal and farm information</p>
      </div>

      <div className="auth-container" style={{ maxWidth: '600px', animation: 'none', opacity: 1, transform: 'none' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '30px' }}>
          <div 
            style={{ 
              width: '100px', 
              height: '100px', 
              borderRadius: '50%', 
              backgroundColor: 'var(--surface-border)',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              overflow: 'hidden',
              cursor: 'pointer'
            }}
            onClick={() => fileInputRef.current.click()}
          >
            {profile?.photoUrl ? (
              <img src={`http://127.0.0.1:8000${profile.photoUrl}`} alt="Profile" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            ) : (
              <span style={{ fontSize: '2rem' }}>👤</span>
            )}
          </div>
          <div>
            <h2 style={{ margin: '0 0 5px 0' }}>{profile?.name}</h2>
            <p style={{ margin: 0, color: 'var(--text-muted)' }}>{profile?.email}</p>
            <button 
              onClick={() => fileInputRef.current.click()}
              style={{ background: 'none', border: 'none', color: 'var(--primary)', cursor: 'pointer', padding: 0, marginTop: '5px' }}
            >
              Change Photo
            </button>
            <input 
              type="file" 
              ref={fileInputRef} 
              style={{ display: 'none' }} 
              accept="image/*"
              onChange={handlePhotoUpload}
            />
          </div>
        </div>

        {error && <div className="error-message" style={{ marginBottom: '20px' }}>{error}</div>}
        {successMsg && <div style={{ color: '#10b981', background: 'rgba(16, 185, 129, 0.1)', padding: '10px', borderRadius: '8px', marginBottom: '20px' }}>{successMsg}</div>}

        <form onSubmit={handleUpdate} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Full Name</label>
            <input 
              type="text" 
              name="name" 
              value={formData.name} 
              onChange={handleChange} 
              className="auth-input" 
              required
            />
          </div>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Age</label>
            <input 
              type="number" 
              name="age" 
              value={formData.age} 
              onChange={handleChange} 
              className="auth-input" 
              required
            />
          </div>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Primary Crop Type</label>
            <input 
              type="text" 
              name="cropType" 
              value={formData.cropType} 
              onChange={handleChange} 
              className="auth-input" 
            />
          </div>
          <div>
            <label style={{ display: 'block', color: 'var(--text-main)', marginBottom: '8px' }}>Land Size (acres)</label>
            <input 
              type="number" 
              name="landSize" 
              value={formData.landSize} 
              onChange={handleChange} 
              className="auth-input" 
              step="0.01"
            />
          </div>
          
          <button 
            type="submit" 
            className="submit-btn" 
            disabled={updating}
            style={{ marginTop: '10px' }}
          >
            {updating ? 'Saving...' : 'Save Profile'}
          </button>
          
          <button 
            type="button" 
            onClick={handleLogout}
            style={{ 
              marginTop: '10px', 
              padding: '12px 24px', 
              backgroundColor: 'transparent', 
              border: '1px solid #ef4444', 
              color: '#ef4444', 
              borderRadius: '8px', 
              cursor: 'pointer',
              fontWeight: '500',
              width: '100%',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.1)'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
          >
            Log Out
          </button>
        </form>
      </div>
    </div>
  );
};

export default Profile;
