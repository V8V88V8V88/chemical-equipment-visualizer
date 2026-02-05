import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import type { Equipment } from '../../types';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface ParameterChartProps {
  equipment: Equipment[];
}

export default function ParameterChart({ equipment }: ParameterChartProps) {
  const labels = equipment.map((e) => e.equipment_name);

  const data = {
    labels,
    datasets: [
      {
        label: 'Flowrate',
        data: equipment.map((e) => e.flowrate),
        borderColor: '#4f46e5',
        backgroundColor: 'rgba(79, 70, 229, 0.08)',
        tension: 0.35,
        borderWidth: 2,
        pointRadius: 2.5,
        pointHoverRadius: 4,
      },
      {
        label: 'Pressure',
        data: equipment.map((e) => e.pressure),
        borderColor: '#64748b',
        backgroundColor: 'rgba(100, 116, 139, 0.08)',
        tension: 0.35,
        borderWidth: 2,
        pointRadius: 2.5,
        pointHoverRadius: 4,
      },
      {
        label: 'Temperature',
        data: equipment.map((e) => e.temperature),
        borderColor: '#334155',
        backgroundColor: 'rgba(51, 65, 85, 0.08)',
        tension: 0.35,
        borderWidth: 2,
        pointRadius: 2.5,
        pointHoverRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          boxWidth: 10,
          padding: 14,
          font: { size: 11 },
          color: '#64748b',
        },
      },
      title: {
        display: true,
        text: 'Equipment Parameters',
        font: { size: 14, weight: 'bold' as const },
        color: '#0f172a',
        padding: { bottom: 12 },
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: {
          font: { size: 11 },
          color: '#64748b',
          maxRotation: 45,
          minRotation: 45,
        },
      },
      y: {
        grid: { color: '#f1f5f9' },
        ticks: {
          font: { size: 11 },
          color: '#64748b',
        },
      },
    },
  };

  return (
    <div style={{ height: '350px' }}>
      <Line data={data} options={options} />
    </div>
  );
}
