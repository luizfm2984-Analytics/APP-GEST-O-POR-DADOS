@echo off
echo ===================================
echo   Iniciando Backend FastAPI
echo   Versao Corrigida
echo ===================================
echo.

cd /d %~dp0

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

REM Criar venv se nao existe
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv usando python direto
echo.
echo Ativando ambiente virtual e instalando dependencias...
echo.

REM Instalar/atualizar dependencias
venv\Scripts\python.exe -m pip install --upgrade pip -q
venv\Scripts\python.exe -m pip install fastapi uvicorn sqlalchemy pydantic "pydantic[email]" python-dotenv email-validator -q

echo.
echo Executando seed do banco...
echo.

REM Configurar PYTHONPATH e executar seed
set PYTHONPATH=%CD%
venv\Scripts\python.exe backend\seed_data.py

if errorlevel 1 (
    echo.
    echo ERRO ao executar seed. Continuando mesmo assim...
    echo.
)

echo.
echo ===================================
echo   Iniciando servidor na porta 8000
echo ===================================
echo.
echo Acesse: http://localhost:8000
echo Documentacao: http://localhost:8000/docs
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

REM Iniciar servidor com PYTHONPATH configurado
set PYTHONPATH=%CD%
venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

pause
