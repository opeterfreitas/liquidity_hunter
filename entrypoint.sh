#!/bin/bash

echo "🔧 Inicializando banco de dados (init_db)..."
python -m db.init_db

echo "🚀 Iniciando Liquidity Hunter..."
python main.py
