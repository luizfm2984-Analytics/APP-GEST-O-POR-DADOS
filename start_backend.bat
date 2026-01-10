@echo off
echo ===================================
echo   Iniciando Backend FastAPI
echo ===================================
echo.

cd /d %~dp0

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

REM Verificar se venv existe, se nao, criar
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv
call venv\Scripts\activate.bat

REM Instalar dependencias
echo.
echo Instalando dependencias...
pip install -q -r requirements.txt

echo.
echo Iniciando servidor na porta 8000...
echo Acesse: http://localhost:8000
echo Documentacao: http://localhost:8000/docs
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

REM Executar seed (primeira vez)
python backend/seed_data.py

REM Iniciar servidor
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

pause
