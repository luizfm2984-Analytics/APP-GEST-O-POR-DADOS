#!/bin/bash

echo "==================================="
echo "  Iniciando Backend FastAPI"
echo "==================================="
echo

cd "$(dirname "$0")"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python não encontrado!"
    echo "Por favor, instale Python 3.8+ e tente novamente."
    exit 1
fi

# Verificar se venv existe, se não, criar
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar venv
source venv/bin/activate

# Instalar dependências
echo
echo "Instalando dependências..."
pip install -q -r requirements.txt

echo
echo "Iniciando servidor na porta 8000..."
echo "Acesse: http://localhost:8000"
echo "Documentação: http://localhost:8000/docs"
echo
echo "Pressione Ctrl+C para parar o servidor"
echo

# Executar seed (primeira vez)
python3 backend/seed_data.py

# Iniciar servidor
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
