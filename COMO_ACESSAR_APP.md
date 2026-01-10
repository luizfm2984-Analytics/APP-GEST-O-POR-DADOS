# 🚀 COMO ACESSAR SEU APP E VER AS TABELAS

## ✅ PASSOS PARA ACESSAR:

### **1. Abrir o App no Navegador**

Abra seu navegador (Chrome, Edge, Firefox) e acesse:

```
http://localhost:5173
```

**OU** se estiver usando outra porta, veja no terminal do frontend qual porta foi usada (5174, 5175, etc.)

---

### **2. Fazer Login**

Você vai ver a tela de login. Use estas credenciais:

**Email:** `admin@fmanalytics.com`  
**Senha:** `admin123`

**⚠️ IMPORTANTE:** Estas credenciais já estão configuradas no banco de dados (foram criadas pelo seed).

---

### **3. Depois do Login**

Após fazer login com sucesso, você será redirecionado para:

**Dashboard:** `http://localhost:5173/dashboard`

---

## 📊 COMO VER AS TABELAS/DADOS:

### **Opção 1: Pelo Frontend (Interface do App)**

Depois de fazer login, você verá um menu lateral com estas opções:

1. **📊 Dashboard** - Visão geral com gráficos e KPIs
2. **📦 Produtos** - Ver/cadastrar produtos
3. **💰 Vendas** - Ver/cadastrar vendas
4. **👥 Clientes** - Ver/cadastrar clientes
5. **📦 Estoque** - Ver estoque e movimentações
6. **👤 Usuários** - Gerenciar usuários do sistema

**Para ver as tabelas:**
- Clique em qualquer item do menu (ex: "Produtos")
- Você verá uma tabela com todos os dados
- Pode adicionar, editar ou deletar itens

---

### **Opção 2: Pelo Backend (API Direta)**

Você pode ver os dados diretamente pela API:

#### **Ver todas as categorias:**
```
http://localhost:8000/api/categorias
```

#### **Ver todos os produtos:**
```
http://localhost:8000/api/produtos
```

#### **Ver todos os clientes:**
```
http://localhost:8000/api/clientes
```

#### **Ver todas as vendas:**
```
http://localhost:8000/api/vendas
```

#### **Ver todo o estoque:**
```
http://localhost:8000/api/estoque
```

#### **Ver todos os usuários:**
```
http://localhost:8000/api/usuarios
```

---

### **Opção 3: Documentação Interativa (Swagger)**

Acesse a documentação completa da API:

```
http://localhost:8000/docs
```

Lá você pode:
- ✅ Ver todos os endpoints
- ✅ Testar requisições
- ✅ Ver os dados retornados
- ✅ Fazer requisições GET, POST, PUT, DELETE

**Passos:**
1. Abra: `http://localhost:8000/docs`
2. Clique em qualquer endpoint (ex: `GET /api/produtos`)
3. Clique em "Try it out"
4. Clique em "Execute"
5. Veja os dados retornados abaixo

---

### **Opção 4: Ver Dados Direto do Banco (SQLite)**

Se quiser ver os dados direto do banco de dados:

#### **Usar ferramenta visual:**

**Recomendado: DB Browser for SQLite** (grátis)
1. Baixe: https://sqlitebrowser.org/
2. Abra o arquivo: `D:\FM\fmanalytics\fmanalytics.db`
3. Veja todas as tabelas e dados

#### **Usar Python (linha de comando):**

```powershell
cd D:\FM\fmanalytics
$env:PYTHONPATH = "D:\FM\fmanalytics"
.\venv\Scripts\python.exe -c "from backend.database import SessionLocal; from backend.models import *; db = SessionLocal(); print('Categorias:', db.query(Category).count()); print('Produtos:', db.query(Product).count()); print('Clientes:', db.query(Client).count()); print('Vendas:', db.query(Sale).count())"
```

---

## 🎯 DADOS QUE JÁ ESTÃO NO BANCO (criados pelo seed):

Após executar o seed, você já tem:

- ✅ **4 categorias:** Alimentação, Balcão, Industrializados, Estufa
- ✅ **3 usuários:** Admin, Carlos Vendedor, Maria Estoquista
- ✅ **5 clientes:** João Silva, Maria Santos, Pedro Oliveira, Ana Costa, Carlos Ferreira
- ✅ **5 produtos:** Pão Francês, Cigarro de Palha, Café, Pastel, Refrigerante
- ✅ **2 vendas:** Exemplos de vendas realizadas
- ✅ **Estoque:** Quantidades iniciais configuradas

---

## 🐛 PROBLEMAS COMUNS:

### **Problema: "Tela em branco" ou erro no frontend**

**Soluções:**
1. Veja o Console do navegador (F12 → Console)
2. Verifique se o frontend está rodando: `http://localhost:5173`
3. Veja o terminal do frontend para erros

### **Problema: "Email ou senha incorretos"**

**Soluções:**
1. Verifique se digitou corretamente:
   - Email: `admin@fmanalytics.com`
   - Senha: `admin123`
2. Verifique se o seed foi executado (deve ter dados no banco)
3. Execute o seed novamente:
   ```powershell
   cd D:\FM\fmanalytics
   $env:PYTHONPATH = "D:\FM\fmanalytics"
   .\venv\Scripts\python.exe backend\seed_data.py
   ```

### **Problema: "Não vejo nenhum dado nas tabelas"**

**Soluções:**
1. O frontend ainda usa `localStorage`, não a API ainda
2. Os dados devem aparecer automaticamente (foram carregados pelo seed no contexto)
3. Se não aparecer, execute o seed novamente

---

## 📝 PRÓXIMOS PASSOS:

1. ✅ **Acessar app:** `http://localhost:5173`
2. ✅ **Fazer login:** `admin@fmanalytics.com` / `admin123`
3. ✅ **Ver dados:** Navegue pelo menu lateral
4. 🔄 **Integrar com API:** Migrar frontend para usar API real (opcional)

---

## 🔗 LINKS RÁPIDOS:

- **Frontend:** http://localhost:5173
- **Backend Docs:** http://localhost:8000/docs
- **API Categorias:** http://localhost:8000/api/categorias
- **API Produtos:** http://localhost:8000/api/produtos
- **API Clientes:** http://localhost:8000/api/clientes
- **API Vendas:** http://localhost:8000/api/vendas

---

**🎉 Agora você sabe como acessar e ver todas as tabelas!**
