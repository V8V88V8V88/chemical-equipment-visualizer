import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface TypeDistributionChartProps {
  distribution: Record<string, number>;
}

export default function TypeDistributionChart({ distribution }: TypeDistributionChartProps) {
  const labels = Object.keys(distribution);
  const values = Object.values(distribution);

  const palette = [
    'rgba(79, 70, 229, 0.75)',
    'rgba(100, 116, 139, 0.75)',
    'rgba(51, 65, 85, 0.75)',
    'rgba(71, 85, 105, 0.75)',
    'rgba(148, 163, 184, 0.75)',
    'rgba(99, 102, 241, 0.75)',
    'rgba(129, 140, 248, 0.75)',
    'rgba(71, 85, 105, 0.65)',
    'rgba(100, 116, 139, 0.65)',
    'rgba(148, 163, 184, 0.65)',
    'rgba(79, 70, 229, 0.6)',
    'rgba(99, 102, 241, 0.6)',
    'rgba(51, 65, 85, 0.6)',
    'rgba(71, 85, 105, 0.6)',
    'rgba(129, 140, 248, 0.6)',
  ];

  const data = {
    labels,
    datasets: [
      {
        label: 'Equipment Count',
        data: values,
        backgroundColor: labels.map((_, i) => palette[i % palette.length]),
        borderRadius: 6,
        borderSkipped: false,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: 'Equipment Type Distribution',
        font: { size: 14, weight: 'bold' as const },
        color: '#0f172a',
        padding: { bottom: 16 },
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: {
          font: { size: 11 },
          color: '#64748b',
          maxRotation: 45,
        },
      },
      y: {
        beginAtZero: true,
        grid: { color: '#f1f5f9' },
        ticks: {
          stepSize: 1,
          font: { size: 11 },
          color: '#64748b',
        },
      },
    },
  };

  return (
    <div style={{ height: '300px' }}>
      <Bar data={data} options={options} />
    </div>
  );
}
