#!/bin/bash

# Start all services for Chemical Equipment Visualizer

set -e

echo "Starting Chemical Equipment Visualizer..."

# Start backend
echo "1. Starting backend server..."
cd backend/server
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!
cd ../..

# Start web frontend
echo "2. Starting web frontend..."
cd web-frontend
bun run dev &
WEB_PID=$!
cd ..

# Wait a moment for services to start
sleep 3

echo ""
echo "Services started:"
echo "- Backend: http://localhost:8000"
echo "- Web App: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services"

# Cleanup on exit
trap "kill $BACKEND_PID $WEB_PID 2>/dev/null; exit" INT TERM

# Wait for background processes
wait