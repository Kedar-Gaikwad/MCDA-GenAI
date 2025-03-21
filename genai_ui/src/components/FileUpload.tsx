import { useState, useCallback } from 'react';
import './FileUpload.css';

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

interface FileUploadProps {
  onReportData: (data: MedicalReportData) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onReportData }) => {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string>('');

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === 'text/plain') {
      setFile(droppedFile);
      setUploadStatus('');
    } else {
      setUploadStatus('Please upload only .txt files');
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile && selectedFile.type === 'text/plain') {
      setFile(selectedFile);
      setUploadStatus('');
    } else {
      setUploadStatus('Please upload only .txt files');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus('Please select a file first');
      return;
    }

    try {
      const formData = new FormData();
      formData.append('file', file);

      // Replace 'YOUR_API_ENDPOINT' with your actual API endpoint
      const response = await fetch('YOUR_API_ENDPOINT', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        // Mock response for testing
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        setUploadStatus('File uploaded successfully!');
        onReportData(data); // Pass the data to the parent component
        setFile(null);
      } else {
        setUploadStatus('Error uploading file');
      }
    } catch (error) {
      setUploadStatus('Error uploading file');
      console.error('Upload error:', error);
    }
  };

  return (
    <div className="file-upload-container">
      <div
        className={`drop-zone ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="drop-zone-content">
          <i className="upload-icon">📄</i>
          <p>Drag and drop your .txt file here or</p>
          <input
            type="file"
            accept=".txt"
            onChange={handleFileSelect}
            id="file-input"
            className="file-input"
          />
          <label htmlFor="file-input" className="file-input-label">
            Choose File
          </label>
        </div>
      </div>
      
      {file && (
        <div className="selected-file">
          <p>Selected file: {file.name}</p>
          <button onClick={handleUpload} className="upload-button">
            Upload File
          </button>
        </div>
      )}
      
      {uploadStatus && (
        <p className={`status-message ${uploadStatus.includes('success') ? 'success' : 'error'}`}>
          {uploadStatus}
        </p>
      )}
    </div>
  );
};

export default FileUpload; 