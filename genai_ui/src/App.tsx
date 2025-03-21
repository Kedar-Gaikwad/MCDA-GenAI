import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import './App.css'
import FileUpload from './components/FileUpload'
import MedicalReport from './components/MedicalReport'

interface MedicalReportData {
  patient_info: {
    NAME: string;
    SEX: string;
    AGE: string;
    DATE: string;
    'UHID.NO': string;
    'REF. By': string;
    OTHER: Record<string, string>;
  };
  findings: string[];
  comments: string[];
}

function HomePage() {
  const navigate = useNavigate();
  const [reportData, setReportData] = useState<MedicalReportData | undefined>();

  const handleReportData = (data: MedicalReportData) => {
    setReportData(data);
    navigate('/report', { state: { reportData: data } });
  };

  return (
    <>
      <h1>Osciloist</h1>
      <h3>File upload</h3>
      <FileUpload onReportData={handleReportData} />
    </>
  );
}

function ReportPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const reportData = location.state?.reportData;

  if (!reportData) {
    navigate('/');
    return null;
  }

  return (
    <>
      <h1>Medical Report</h1>
      <button className="back-btn" onClick={() => navigate('/')}>
        ← Back to Upload
      </button>
      <MedicalReport initialData={reportData} />
    </>
  );
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/report" element={<ReportPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App
