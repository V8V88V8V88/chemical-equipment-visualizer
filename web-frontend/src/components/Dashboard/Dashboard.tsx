import { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { datasetApi } from '../../services/api';
import type { DatasetListItem, Dataset } from '../../types';
import CsvUpload from '../Upload/CsvUpload';
import DatasetList from './DatasetList';
import DatasetDetail from './DatasetDetail';
import Footer from '../Footer/Footer';
import './Dashboard.css';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [datasets, setDatasets] = useState<DatasetListItem[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchDatasets = async () => {
    try {
      const data = await datasetApi.list();
      setDatasets(data);
      if (data.length > 0 && !selectedId) {
        setSelectedId(data[0].id);
      }
    } catch (err) {
      console.error('Failed to fetch datasets:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, []);

  const handleUploadSuccess = (dataset: Dataset) => {
    fetchDatasets();
    setSelectedId(dataset.id);
  };

  const handleLogout = async () => {
    await logout();
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Chemical Equipment Visualizer</h1>
        <div className="user-info">
          <span>Welcome, {user?.username}</span>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </header>

      <div className="dashboard-content">
        <aside className="sidebar">
          <CsvUpload onUploadSuccess={handleUploadSuccess} />
          <h3>Recent Datasets</h3>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <DatasetList
              datasets={datasets}
              selectedId={selectedId}
              onSelect={setSelectedId}
            />
          )}
        </aside>

        <main className="main-content">
          {selectedId ? (
            <DatasetDetail datasetId={selectedId} />
          ) : (
            <div className="no-selection">
              <p>Upload a CSV file or select a dataset to view details</p>
            </div>
          )}
        </main>
      </div>

      <Footer />
    </div>
  );
}
