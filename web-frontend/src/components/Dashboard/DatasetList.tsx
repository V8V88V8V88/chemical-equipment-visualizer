import type { DatasetListItem } from '../../types';
import './Dashboard.css';

interface DatasetListProps {
  datasets: DatasetListItem[];
  selectedId: number | null;
  onSelect: (id: number) => void;
}

export default function DatasetList({ datasets, selectedId, onSelect }: DatasetListProps) {
  if (datasets.length === 0) {
    return <p className="no-datasets">No datasets uploaded yet</p>;
  }

  return (
    <ul className="dataset-list">
      {datasets.map((dataset) => (
        <li
          key={dataset.id}
          className={`dataset-item ${selectedId === dataset.id ? 'selected' : ''}`}
          onClick={() => onSelect(dataset.id)}
        >
          <span className="dataset-name">{dataset.name}</span>
          <span className="dataset-meta">
            {dataset.equipment_count} items |{' '}
            {new Date(dataset.uploaded_at).toLocaleDateString()}
          </span>
        </li>
      ))}
    </ul>
  );
}
