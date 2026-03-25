@echo off
echo Starting Stanford AI Manager...

:: Start Backend
start "Backend API" cmd /k "cd app_001_stanford_manager\backend && python main.py"

:: Start Frontend
start "Frontend UI" cmd /k "cd app_001_stanford_manager && npm run dev"

echo App is starting...
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
pause
