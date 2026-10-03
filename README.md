# AgriIntel

**Intelligence for every hectare.**
AgriIntel is a full-stack, AI-powered agricultural intelligence platform designed to connect farmers, markets, and climate data. It provides farm-level clarity and global agribusiness perspectives through machine learning and generative AI.

---

## 🌟 Key Features

1. **Farmer Decision Dashboard**
   - **Manual Data Logging:** Easily log soil moisture, temperature, humidity, and rain detection data.
   - **Chronological Tracking:** All readings are securely tracked and sorted in real-time.

2. **AI Agronomist (Powered by Gemini)**
   - Context-aware crop health recommendations using Google's Gemini Generative AI.
   - Intelligent risk-level assessments (Low/Medium/High) based on live environmental inputs.

3. **Machine Learning Suite**
   - **Yield Prediction:** A trained Scikit-Learn Random Forest Regressor predicts crop yield (kg/acre) based on local farm conditions.
   - **Anomaly Detection:** An Isolation Forest model passively monitors farm data to detect critical environmental anomalies (e.g., severe droughts, sensor malfunctions).

4. **Farm Profitability Calculator**
   - Comprehensive financial modeling in Rupees (₹).
   - Calculates Total Costs, Revenue, Net Profit, Profit Margins, and Break-Even Points based on yield predictions and market prices.

5. **Security & Identity**
   - Secure JWT-based Authentication.
   - Dedicated User Profiles with Profile Photo uploads.
   - Silent **Security Event Auditing** tracking every successful and failed login attempt for system-wide threat monitoring.

---

## 🛠️ Technology Stack

**Frontend (Client)**
- **Framework:** React + Vite
- **Routing:** React Router DOM
- **Networking:** Axios with global interceptors
- **Styling:** Custom CSS implementing a premium Figma-designed B2B SaaS theme (Cream background, Forest Green accents, Playfair Display typography).

**Backend (API)**
- **Framework:** Python + FastAPI
- **Database:** MongoDB Atlas (accessed asynchronously via Motor)
- **Machine Learning:** Scikit-Learn, Pandas, NumPy
- **Generative AI:** `google-generativeai` (Gemini 1.5 Flash)
- **Authentication:** PyJWT, Passlib (Bcrypt)
- **Testing:** Pytest integration suite

---

## 🚀 Setup and Installation (Local Development)

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- A MongoDB Atlas account and connection string
- A Google AI Studio (Gemini) API Key

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd agriintel-backend
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the `agriintel-backend` folder with the following variables:
   ```text
   MONGO_URI=your_mongodb_connection_string
   MONGO_DB_NAME=agriintel
   JWT_SECRET=your_super_secret_key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   GEMINI_API_KEY=your_gemini_api_key
   ```
4. Run the FastAPI development server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
  

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd agriintel-frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Run the Vite development server:
   ```bash
   npm run dev
   ```
   *(The frontend will run on `http://localhost:5173`)*

---

## 🧪 Testing

The backend includes a comprehensive `pytest` integration suite that validates end-to-end functionality across Authentication, Sensors, AI Predictions, Finance, and Notifications.



## 🌐 Deployment Architecture

AgriIntel is configured for modern serverless deployment:
- **Backend:** Designed for deployment on **Render** (Web Service running Uvicorn).
- **Frontend:** Designed for zero-config deployment on **Vercel**.
- **Database:** Fully managed on **MongoDB Atlas**.

