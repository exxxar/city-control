@echo off
echo ========================================
echo   Starting City Under Control
echo ========================================
echo.

:: Start backend in a separate window
echo [1/3] Starting Backend...
start "Backend" cmd /k "cd backend && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

:: Wait 2 seconds for backend to initialize
timeout /t 2 /nobreak >nul

:: Start client in a separate window
echo [2/3] Starting Client...
start "Client" cmd /k "cd client && npm run dev"

:: Start admin in a separate window
echo [3/3] Starting Admin...
start "Admin" cmd /k "cd admin && npm run dev"

echo.
echo ========================================
echo   All services are running!
echo   Backend: http://127.0.0.1:8000
echo   Client:  http://127.0.0.1:5173
echo   Admin:   http://127.0.0.1:5174
echo ========================================
echo.
echo Press any key to exit this window...
pause >nul