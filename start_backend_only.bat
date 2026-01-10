@echo off
title Backend FastAPI - FM Analytics
color 0A

echo ===================================
echo   BACKEND FASTAPI - FM Analytics
echo ===================================
echo.

cd /d %~dp0

REM Configurar PYTHONPATH
set PYTHONPATH=%CD%

REM Verificar se venv existe
if not exist venv (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Execute primeiro: python -m venv venv
    pause
    exit /b 1
)

REM Iniciar servidor
echo Iniciando servidor na porta 8000...
echo.
echo Acesse:
echo   - Health: http://localhost:8000/health
echo   - API Docs: http://localhost:8000/docs
echo   - API: http://localhost:8000/api
echo.
echo Pressione Ctrl+C para parar
echo ===================================
echo.

venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

pause
