@echo off
TITLE Nehru Place IT Services - Local Server
echo =========================================================
echo Starting Nehru Place IT Services (Local Development Server)
echo Website URL: http://127.0.0.1:8000/
echo Admin Panel: http://127.0.0.1:8000/admin/
echo Superuser Credentials: admin / admin123
echo =========================================================
echo.
cd /d "G:\My Drive\ecomnpits\ecomnpits"
python manage.py runserver 0.0.0.0:8000
pause
