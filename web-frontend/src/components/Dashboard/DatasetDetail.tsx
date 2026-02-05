import { useState, useEffect } from 'react';
import { datasetApi } from '../../services/api';
import type { Dataset, Summary } from '../../types';
import TypeDistributionChart from '../Charts/TypeDistributionChart';
import ParameterChart from '../Charts/ParameterChart';
import './Dashboard.css';

interface DatasetDetailProps {
  datasetId: number;
}

export default function DatasetDetail({ datasetId }: DatasetDetailProps) {
  const [dataset, setDataset] = useState<Dataset | null>(null);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [datasetData, summaryData] = await Promise.all([
          datasetApi.get(datasetId),
          datasetApi.getSummary(datasetId),
        ]);
        setDataset(datasetData);
        setSummary(summaryData);
      } catch (err) {
        console.error('Failed to fetch dataset:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [datasetId]);

  const handleDownloadPdf = async () => {
    if (!dataset) return;
    setDownloading(true);
    try {
      await datasetApi.downloadReport(datasetId, dataset.name.replace('.csv', ''));
    } catch (err) {
      console.error('Failed to download report:', err);
    } finally {
      setDownloading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!dataset || !summary) {
    return <div className="error">Failed to load dataset</div>;
  }

  return (
    <div className="dataset-detail">
      <div className="detail-header">
        <h2>{dataset.name}</h2>
        <button onClick={handleDownloadPdf} disabled={downloading} className="pdf-btn">
          {downloading ? 'Generating...' : 'Download PDF'}
        </button>
      </div>

      <div className="summary-cards">
        <div className="summary-card">
          <span className="card-label">Total Equipment</span>
          <span className="card-value">{summary.total_count}</span>
        </div>
        <div className="summary-card">
          <span className="card-label">Avg Flowrate</span>
          <span className="card-value">{summary.avg_flowrate.toFixed(2)}</span>
        </div>
        <div className="summary-card">
          <span className="card-label">Avg Pressure</span>
          <span className="card-value">{summary.avg_pressure.toFixed(2)}</span>
        </div>
        <div className="summary-card">
          <span className="card-label">Avg Temperature</span>
          <span className="card-value">{summary.avg_temperature.toFixed(2)}</span>
        </div>
      </div>

      <div className="charts-container">
        <div className="chart-wrapper">
          <TypeDistributionChart distribution={summary.type_distribution} />
        </div>
        <div className="chart-wrapper">
          <ParameterChart equipment={dataset.equipment} />
        </div>
      </div>

      <div className="data-table-container">
        <h3>Equipment Data</h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Flowrate</th>
              <th>Pressure</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            {dataset.equipment.map((eq) => (
              <tr key={eq.id}>
                <td>{eq.equipment_name}</td>
                <td>{eq.equipment_type}</td>
                <td>{eq.flowrate.toFixed(2)}</td>
                <td>{eq.pressure.toFixed(2)}</td>
                <td>{eq.temperature.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
