import React, { useState, useEffect } from 'react';
import { PDFDownloadLink } from '@react-pdf/renderer';
import './MedicalReport.css';
import MedicalReportPDF from './MedicalReportPDF';

interface PatientInfo {
  NAME: string;
  SEX: string;
  AGE: string;
  DATE: string;
  'UHID.NO': string;
  'REF. By': string;
  OTHER: Record<string, string>;
}

interface MedicalReportData {
  patient_info: PatientInfo;
  findings: string[];
  comments: string[];
}

interface MedicalReportProps {
  initialData?: MedicalReportData;
}

const MedicalReport: React.FC<MedicalReportProps> = ({ initialData }) => {
  const [reportData, setReportData] = useState<MedicalReportData>({
    patient_info: {
      NAME: '',
      SEX: '',
      AGE: '',
      DATE: '',
      'UHID.NO': '',
      'REF. By': '',
      OTHER: {}
    },
    findings: [],
    comments: []
  });

  const [newFieldKey, setNewFieldKey] = useState('');
  const [showNewFieldInput, setShowNewFieldInput] = useState(false);

  useEffect(() => {
    if (initialData) {
      setReportData(initialData);
    }
  }, [initialData]);

  const handlePatientInfoChange = (key: keyof PatientInfo | string, value: string) => {
    setReportData(prev => ({
      ...prev,
      patient_info: {
        ...prev.patient_info,
        ...(key in prev.patient_info
          ? { [key]: value }
          : { OTHER: { ...prev.patient_info.OTHER, [key]: value } })
      }
    }));
  };

  const handleListChange = (
    section: 'findings' | 'comments',
    index: number,
    value: string
  ) => {
    setReportData(prev => ({
      ...prev,
      [section]: prev[section].map((item, i) => (i === index ? value : item))
    }));
  };

  const addListItem = (section: 'findings' | 'comments') => {
    setReportData(prev => ({
      ...prev,
      [section]: [...prev[section], '']
    }));
  };

  const removeListItem = (section: 'findings' | 'comments', index: number) => {
    setReportData(prev => ({
      ...prev,
      [section]: prev[section].filter((_, i) => i !== index)
    }));
  };

  const addCustomField = () => {
    if (newFieldKey.trim()) {
      handlePatientInfoChange(newFieldKey.trim(), '');
      setNewFieldKey('');
      setShowNewFieldInput(false);
    }
  };

  const removeCustomField = (key: string) => {
    setReportData(prev => {
      const newOther = { ...prev.patient_info.OTHER };
      delete newOther[key];
      return {
        ...prev,
        patient_info: {
          ...prev.patient_info,
          OTHER: newOther
        }
      };
    });
  };

  const exportToJSON = () => {
    const jsonString = JSON.stringify(reportData, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'medical_report.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const exportToPDF = () => {
    // This function is no longer needed as we're using PDFDownloadLink
  };

  if (!initialData) {
    return null; // Don't render until we have initial data
  }

  return (
    <div className="medical-report">
      <h2>Osciloist Medical Report</h2>
      
      <section className="patient-info">
        <h3>Patient Information</h3>
        <div className="info-grid">
          {Object.entries(reportData.patient_info)
            .filter(([key]) => key !== 'OTHER')
            .map(([key, value]) => (
              <div key={key} className="info-field">
                <label>{key}:</label>
                <input
                  type="text"
                  value={value}
                  onChange={(e) => handlePatientInfoChange(key as keyof PatientInfo, e.target.value)}
                />
              </div>
            ))}
          
          {/* Custom fields from OTHER */}
          {Object.entries(reportData.patient_info.OTHER).map(([key, value]) => (
            <div key={key} className="info-field custom-field">
              <label>{key}:</label>
              <div className="custom-field-input">
                <input
                  type="text"
                  value={value}
                  onChange={(e) => handlePatientInfoChange(key, e.target.value)}
                />
                <button
                  className="remove-btn small"
                  onClick={() => removeCustomField(key)}
                  title="Remove field"
                >
                  ×
                </button>
              </div>
            </div>
          ))}
        </div>

        {showNewFieldInput ? (
          <div className="add-field-form">
            <input
              type="text"
              value={newFieldKey}
              onChange={(e) => setNewFieldKey(e.target.value)}
              placeholder="Enter field name"
              className="new-field-input"
            />
            <button className="add-btn" onClick={addCustomField}>
              Add
            </button>
            <button className="cancel-btn" onClick={() => {
              setShowNewFieldInput(false);
              setNewFieldKey('');
            }}>
              Cancel
            </button>
          </div>
        ) : (
          <button className="add-btn" onClick={() => setShowNewFieldInput(true)}>
            + Add Custom Field
          </button>
        )}
      </section>

      <div className="findings-comments-container">
        <section className="findings">
          <h3>Findings</h3>
          {reportData.findings.map((finding, index) => (
            <div key={index} className="list-item">
              <textarea
                value={finding}
                onChange={(e) => handleListChange('findings', index, e.target.value)}
                rows={2}
              />
              <button
                className="remove-btn"
                onClick={() => removeListItem('findings', index)}
              >
                Remove
              </button>
            </div>
          ))}
          <button className="add-btn" onClick={() => addListItem('findings')}>
            Add Finding
          </button>
        </section>

        <section className="comments">
          <h3>Comments</h3>
          {reportData.comments.map((comment, index) => (
            <div key={index} className="list-item">
              <textarea
                value={comment}
                onChange={(e) => handleListChange('comments', index, e.target.value)}
                rows={2}
              />
              <button
                className="remove-btn"
                onClick={() => removeListItem('comments', index)}
              >
                Remove
              </button>
            </div>
          ))}
          <button className="add-btn" onClick={() => addListItem('comments')}>
            Add Comment
          </button>
        </section>
      </div>

      <PDFDownloadLink
        document={<MedicalReportPDF data={reportData} />}
        fileName="medical_report.pdf"
        className="export-btn"
      >
        {({ loading }) => (loading ? 'Generating PDF...' : 'Export to PDF')}
      </PDFDownloadLink>
    </div>
  );
};

export default MedicalReport; 