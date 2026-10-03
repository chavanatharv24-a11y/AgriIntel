import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Diagnose from './pages/Diagnose';
import Market from './pages/Market';
import Assistant from './pages/Assistant';
import Finance from './pages/Finance';
import LogReading from './pages/LogReading';
import Profile from './pages/Profile';
import Layout from './components/Layout';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/diagnose" element={<Diagnose />} />
          <Route path="/market" element={<Market />} />
          <Route path="/assistant" element={<Assistant />} />
          <Route path="/finance" element={<Finance />} />
          <Route path="/log-reading" element={<LogReading />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
