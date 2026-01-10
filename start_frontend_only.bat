@echo off
title Frontend React/Vite - FM Analytics
color 0B

echo ===================================
echo   FRONTEND REACT/VITE - FM Analytics
echo ===================================
echo.

cd /d %~dp0

REM Verificar se node_modules existe
if not exist node_modules (
    echo Instalando dependencias...
    call npm install
    echo.
)

REM Iniciar servidor
echo Iniciando servidor na porta 5173...
echo.
echo Acesse: http://localhost:5173
echo.
echo Pressione Ctrl+C para parar
echo ===================================
echo.

call npm run dev

pause
