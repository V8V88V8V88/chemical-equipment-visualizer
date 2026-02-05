# Chemical Equipment Visualizer

A hybrid web + desktop app for visualizing chemical equipment data from CSV files.

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Web Frontend**: React + Chart.js + Vite
- **Desktop Frontend**: PyQt5 + Matplotlib
- **Database**: SQLite

## Setup

### Backend

```bash
cd backend/server
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Runs on http://localhost:8000

### Web Frontend

```bash
cd web-frontend
bun install  # or npm install (I prefer bun :P)
bun run dev  # or npm run dev
```

Runs on http://localhost:5173

### Desktop App

```bash
cd desktop-app
pip install -r requirements.txt
python main.py
```

## CSV Format

The CSV file should have these columns:

| Equipment Name | Type | Flowrate | Pressure | Temperature |
|----------------|------|----------|----------|-------------|
| Pump P-101 | Centrifugal Pump | 150.5 | 3.2 | 45.0 |

See `sample_equipment_data.csv` for example data.

## Features

- Upload CSV files with equipment data
- View summary stats (averages, counts)
- Charts showing type distribution and parameter trends
- Download PDF reports
- Keeps last 5 uploaded datasets per user
- User authentication (register/login)

## API Endpoints

- `POST /api/auth/register/` - Register
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/upload/` - Upload CSV
- `GET /api/datasets/` - List datasets
- `GET /api/datasets/<id>/` - Dataset details
- `GET /api/datasets/<id>/summary/` - Stats
- `GET /api/datasets/<id>/report/` - Download PDF
