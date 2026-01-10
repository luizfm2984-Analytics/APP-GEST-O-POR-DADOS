"""Script simples para ver dados do banco"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal
from backend.models import Category, Product, Client, Sale, User, Stock

db = SessionLocal()

try:
    print("=" * 50)
    print("  DADOS NO BANCO DE DADOS")
    print("=" * 50)
    print()
    
    cats = db.query(Category).count()
    prods = db.query(Product).count()
    clis = db.query(Client).count()
    sales = db.query(Sale).count()
    users = db.query(User).count()
    stock = db.query(Stock).count()
    
    print(f"📊 Resumo:")
    print(f"  - Categorias: {cats}")
    print(f"  - Produtos: {prods}")
    print(f"  - Clientes: {clis}")
    print(f"  - Vendas: {sales}")
    print(f"  - Usuários: {users}")
    print(f"  - Itens de Estoque: {stock}")
    print()
    
    if users > 0:
        print("👤 USUÁRIOS DISPONÍVEIS:")
        print("-" * 50)
        for user in db.query(User).all():
            print(f"  Email: {user.email}")
            print(f"  Senha: {user.password}")
            print(f"  Nome: {user.name}")
            print()
    
    if prods > 0:
        print("📦 PRODUTOS (primeiros 3):")
        print("-" * 50)
        for prod in db.query(Product).limit(3).all():
            print(f"  - {prod.name} (SKU: {prod.sku}) - R$ {prod.sell_price}")
        print()
    
    print("=" * 50)
    print("✅ Dados verificados com sucesso!")
    print()
    print("🔑 CREDENCIAIS DE LOGIN:")
    print("  Email: admin@fmanalytics.com")
    print("  Senha: admin123")
    print()
    print("🌐 ACESSE O APP:")
    print("  Frontend: http://localhost:5173")
    print("  Backend: http://localhost:8000/docs")
    
finally:
    db.close()
