import { useState, useRef } from 'react';
import { datasetApi } from '../../services/api';
import type { Dataset } from '../../types';
import './CsvUpload.css';

interface CsvUploadProps {
  onUploadSuccess: (dataset: Dataset) => void;
}

export default function CsvUpload({ onUploadSuccess }: CsvUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    if (!file.name.endsWith('.csv')) {
      setError('Please upload a CSV file');
      return;
    }
    setError('');
    setUploading(true);
    try {
      const dataset = await datasetApi.upload(file);
      onUploadSuccess(dataset);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { error?: string } } };
      setError(error.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  return (
    <div className="upload-container">
      <div
        className={`drop-zone ${isDragging ? 'dragging' : ''} ${uploading ? 'uploading' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          hidden
        />
        {uploading ? (
          <p>Uploading...</p>
        ) : (
          <>
            <p>Drag & drop a CSV file here</p>
            <p>or click to select</p>
          </>
        )}
      </div>
      {error && <div className="upload-error">{error}</div>}
    </div>
  );
}
