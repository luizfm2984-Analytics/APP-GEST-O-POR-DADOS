import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import date

# =====================================================
# CONFIGURAÇÃO E IDENTIDADE VISUAL
# =====================================================
st.set_page_config(page_title="FM Analytics | Gestão", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; border-left: 5px solid #001f3f; padding: 15px; border-radius: 10px; }
    div.stButton > button:first-child { background-color: #001f3f; color: white; border-radius: 8px; width: 100%; }
    div.stButton > button[kind="primary"] { background-color: #ff4b4b !important; color: white !important; border: none; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# CONEXÃO COM BANCO (DISCO D:)
# =====================================================
DATABASE_URL = "postgresql+psycopg2://postgres:Luizfm2984@localhost:5432/meuapponline"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================
def carregar_dados(query):
    return pd.read_sql(query, engine)

def executar_sql(sql, params=None):
    if params is None:
        params = {}
    with engine.begin() as conn:
        conn.execute(text(sql), params)

# =====================================================
# NAVEGAÇÃO
# =====================================================
with st.sidebar:
    st.markdown("# 🧠 FM Analytics")
    st.caption("Gestão Baseada em Dados")
    st.divider()
    pagina = st.radio("Navegação:", 
                      ["📊 Dashboard", "📦 Estoque Geral", "👥 Equipe", "💰 Vendas/Caixa", "📤 Importar Dados"])

# =====================================================
# 1. DASHBOARD
# =====================================================
if pagina == "📊 Dashboard":
    st.title("📊 Dashboard Executivo")
    
    df_v = carregar_dados("SELECT total_liquido, margem, data_venda FROM vendas")
    
    if not df_v.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento Total", f"R$ {df_v['total_liquido'].sum():,.2f}")
        c2.metric("Margem Total", f"R$ {df_v['margem'].sum():,.2f}")
        c3.metric("Ticket Médio", f"R$ {df_v['total_liquido'].mean():,.2f}")
        
        st.divider()
        st.subheader("Faturamento Diário")
        chart_data = df_v.groupby('data_venda')['total_liquido'].sum()
        st.line_chart(chart_data)
    else:
        st.info("📊 Aguardando primeiras vendas para gerar inteligência...")

# =====================================================
# 2. ESTOQUE GERAL (COM SELEÇÃO DINÂMICA E EXCLUSÃO EM MASSA)
# =====================================================
elif pagina == "📦 Estoque Geral":
    st.title("📦 Estoque Geral")
    
    aba_lista, aba_cad = st.tabs(["🔎 Consultar e Excluir", "➕ Novo Item"])
    
    with aba_lista:
        # Carregar dados
        df = carregar_dados("""
            SELECT id, codigo, nome, categoria, preco_venda, preco_custo 
            FROM produtos 
            WHERE ativo = TRUE 
            ORDER BY nome
        """)
        
        if not df.empty:
            # Filtro por categoria
            col_f1, _ = st.columns([2, 4])
            categorias = sorted(df['categoria'].dropna().unique().tolist())
            filtro_cat = col_f1.multiselect("Filtrar por Categoria", options=categorias)
            
            # Aplicar filtro
            df_filtrado = df.copy()
            if filtro_cat:
                df_filtrado = df_filtrado[df_filtrado['categoria'].isin(filtro_cat)]
            
            # Inicializar estado de seleção
            if 'sel_tudo_estoque' not in st.session_state:
                st.session_state.sel_tudo_estoque = False
            
            # Botões de seleção
            c_sel1, c_sel2, _ = st.columns([1.5, 1.5, 4])
            if c_sel1.button("✅ Selecionar Tudo"):
                st.session_state.sel_tudo_estoque = True
                st.rerun()
            if c_sel2.button("❌ Desmarcar"):
                st.session_state.sel_tudo_estoque = False
                st.rerun()
            
            # Adicionar coluna de checkbox
            df_filtrado.insert(0, "Sel.", st.session_state.sel_tudo_estoque)
            
            # Editor de dados com checkbox
            df_editado = st.data_editor(
                df_filtrado,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Sel.": st.column_config.CheckboxColumn("Selecionar para Excluir"),
                    "id": None,
                    "preco_venda": st.column_config.NumberColumn("Preço Venda", format="R$ %.2f"),
                    "preco_custo": st.column_config.NumberColumn("Preço Custo", format="R$ %.2f")
                }
            )
            
            # Processar exclusão em massa
            selecionados = df_editado[df_editado["Sel."] == True]["id"].tolist()
            
            if selecionados:
                st.warning(f"⚠️ {len(selecionados)} item(ns) selecionado(s) para exclusão")
                if st.button(f"🗑️ EXCLUIR {len(selecionados)} ITEM(NS)", type="primary"):
                    with st.spinner("Excluindo..."):
                        for item_id in selecionados:
                            executar_sql("UPDATE produtos SET ativo = FALSE WHERE id = :id", {"id": item_id})
                        st.session_state.sel_tudo_estoque = False
                        st.success(f"✅ {len(selecionados)} item(ns) excluído(s) com sucesso!")
                        st.rerun()
        else:
            st.info("📦 Nenhum produto cadastrado no estoque.")
    
    with aba_cad:
        st.subheader("Cadastrar Novo Produto")
        with st.form("form_cad_produto"):
            col1, col2 = st.columns(2)
            nome = col1.text_input("Nome do Produto *", placeholder="Ex: Notebook Dell")
            codigo = col2.text_input("Código/SKU", placeholder="Ex: PROD001")
            categoria = col1.text_input("Categoria", placeholder="Ex: Eletrônicos")
            preco_venda = col2.number_input("Preço de Venda (R$) *", min_value=0.0, step=0.01, format="%.2f")
            preco_custo = col1.number_input("Preço de Custo (R$)", min_value=0.0, step=0.01, format="%.2f")
            
            if st.form_submit_button("💾 Salvar Produto"):
                if nome and preco_venda > 0:
                    executar_sql("""
                        INSERT INTO produtos (empresa_id, nome, codigo, categoria, preco_venda, preco_custo, ativo)
                        VALUES (1, :nome, :codigo, :categoria, :venda, :custo, TRUE)
                    """, {
                        "nome": nome,
                        "codigo": codigo if codigo else "",
                        "categoria": categoria if categoria else "Geral",
                        "venda": preco_venda,
                        "custo": preco_custo
                    })
                    st.success("✅ Produto cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("⚠️ Preencha o nome e o preço de venda")

# =====================================================
# 3. EQUIPE
# =====================================================
elif pagina == "👥 Equipe":
    st.title("👥 Gestão de Equipe")
    
    with st.expander("➕ Cadastrar Novo Funcionário", expanded=False):
        with st.form("form_funcionario"):
            col1, col2 = st.columns(2)
            nome_func = col1.text_input("Nome Completo *", placeholder="Ex: João Silva")
            cargo = col2.selectbox("Cargo", ["Vendedor", "Gerente", "Operador", "Supervisor"])
            
            if st.form_submit_button("💾 Salvar Colaborador"):
                if nome_func:
                    executar_sql("""
                        INSERT INTO funcionarios (empresa_id, nome, cargo, ativo)
                        VALUES (1, :nome, :cargo, TRUE)
                    """, {"nome": nome_func, "cargo": cargo})
                    st.success("✅ Funcionário cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("⚠️ Preencha o nome do funcionário")
    
    st.subheader("Lista de Funcionários")
    df_func = carregar_dados("SELECT id, nome, cargo FROM funcionarios WHERE ativo = TRUE ORDER BY nome")
    if not df_func.empty:
        st.dataframe(df_func, use_container_width=True, hide_index=True)
    else:
        st.info("👥 Nenhum funcionário cadastrado.")

# =====================================================
# 4. VENDAS/CAIXA (PDV COMPLETO)
# =====================================================
elif pagina == "💰 Vendas/Caixa":
    st.title("💰 Ponto de Venda (PDV)")
    
    df_p = carregar_dados("SELECT id, nome, preco_venda, preco_custo FROM produtos WHERE ativo = TRUE ORDER BY nome")
    df_f = carregar_dados("SELECT id, nome FROM funcionarios WHERE ativo = TRUE ORDER BY nome")
    
    if df_p.empty or df_f.empty:
        st.warning("⚠️ Certifique-se de ter Produtos e Funcionários cadastrados antes de registrar vendas!")
    else:
        with st.form("form_pdv_multi"):
            # Cliente e Vendedor
            ctop1, ctop2, ctop3 = st.columns([3, 2, 2])
            cliente_nome = ctop1.text_input("Nome do Cliente (opcional)", placeholder="Ex: Maria Souza")
            cliente_tel = ctop2.text_input("Celular (opcional)", placeholder="Ex: 11 99999-9999")
            vendedor_nome = ctop3.selectbox("Vendedor *", df_f['nome'].tolist())

            st.divider()

            # Seleção de produtos
            nomes_produtos = df_p['nome'].tolist()
            sel = st.multiselect("Selecione os Produtos", nomes_produtos, key="sel_produtos")

            itens = []
            total_bruto = 0.0
            total_custo = 0.0

            if sel:
                st.markdown("**Produtos Selecionados:**")
                for idx, nome in enumerate(sel):
                    linha = df_p[df_p['nome'] == nome].iloc[0]
                    pid = int(linha['id'])
                    colq1, colq2, colq3, colq4 = st.columns([4, 2, 2, 2])
                    colq1.write(f"**{nome}**")
                    qtd = colq2.number_input("Qtd", min_value=1, value=1, step=1, key=f"qtd_{pid}_{idx}")
                    preco = float(linha['preco_venda'])
                    custo = float(linha['preco_custo'])
                    colq3.metric("Preço", f"R$ {preco:,.2f}")
                    subtotal = qtd * preco
                    colq4.metric("Subtotal", f"R$ {subtotal:,.2f}")

                    itens.append({
                        "produto_id": pid,
                        "nome": nome,
                        "quantidade": qtd,
                        "preco_unitario": preco,
                        "custo_unitario": custo,
                        "subtotal": subtotal,
                        "subtotal_custo": qtd * custo
                    })
                    total_bruto += subtotal
                    total_custo += qtd * custo

            desconto = st.number_input("Desconto Total (R$)", min_value=0.0, step=0.01, format="%.2f", key="desconto_pdv")
            total_liquido = max(total_bruto - desconto, 0.0)
            margem = total_liquido - total_custo

            st.divider()
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Bruto", f"R$ {total_bruto:,.2f}")
            m2.metric("Total Líquido", f"R$ {total_liquido:,.2f}")
            m3.metric("Margem", f"R$ {margem:,.2f}")

            btn_finalizar = st.form_submit_button("🚀 FINALIZAR VENDA", use_container_width=True, disabled=(len(itens) == 0))

        if btn_finalizar:
            # Recalcular itens com base na seleção atual (valores do form)
            # Precisamos recriar a lista de itens porque os valores podem ter mudado
            itens_final = []
            total_bruto_final = 0.0
            total_custo_final = 0.0
            
            # Recriar lista de produtos selecionados
            # Como estamos fora do form, precisamos usar session_state ou recriar
            # Vamos usar uma abordagem mais simples: recriar baseado nos produtos disponíveis
            sel_final = sel if 'sel' in locals() else []
            
            if not sel_final or len(sel_final) == 0:
                st.error("⚠️ Selecione pelo menos um produto!")
                st.stop()
            
            # Recalcular itens com as quantidades finais
            for idx, nome in enumerate(sel_final):
                linha = df_p[df_p['nome'] == nome].iloc[0]
                pid = int(linha['id'])
                # Buscar quantidade do session_state (definida no form)
                qtd_key = f"qtd_{pid}_{idx}"
                qtd = st.session_state.get(qtd_key, 1)
                
                preco = float(linha['preco_venda'])
                custo = float(linha['preco_custo'])
                subtotal = qtd * preco
                
                itens_final.append({
                    "produto_id": pid,
                    "nome": nome,
                    "quantidade": qtd,
                    "preco_unitario": preco,
                    "custo_unitario": custo,
                    "subtotal": subtotal,
                    "subtotal_custo": qtd * custo
                })
                total_bruto_final += subtotal
                total_custo_final += qtd * custo
            
            # Recalcular totais
            desconto_key = "desconto_pdv"
            desconto_final = st.session_state.get(desconto_key, 0.0)
            total_liquido_final = max(total_bruto_final - desconto_final, 0.0)
            margem_final = total_liquido_final - total_custo_final
            
            funcionario_id = int(df_f[df_f['nome'] == vendedor_nome].iloc[0]['id'])
            funcionario_nome = vendedor_nome

            # Buscar ou criar cliente e vendedor ANTES da transação principal
            cliente_id = None
            vendedor_id = None
            
            with engine.begin() as conn:
                # 1. Buscar ou criar cliente (opcional)
                if cliente_nome or cliente_tel:
                    # Tenta achar por telefone primeiro (mais confiável)
                    if cliente_tel:
                        row = conn.execute(text("""
                            SELECT id FROM clientes WHERE empresa_id = 1 AND telefone = :tel AND ativo = TRUE LIMIT 1
                        """), {"tel": cliente_tel}).fetchone()
                        if row:
                            cliente_id = int(row[0])
                    # Se não achou e tem nome, tenta por nome
                    if cliente_id is None and cliente_nome:
                        row = conn.execute(text("""
                            SELECT id FROM clientes WHERE empresa_id = 1 AND nome = :nome AND ativo = TRUE LIMIT 1
                        """), {"nome": cliente_nome}).fetchone()
                        if row:
                            cliente_id = int(row[0])
                    # Se ainda não achou, cria cliente mínimo
                    if cliente_id is None:
                        cliente_id = conn.execute(text("""
                            INSERT INTO clientes (empresa_id, nome, telefone, ativo)
                            VALUES (1, :nome, :tel, TRUE) RETURNING id
                        """), {"nome": cliente_nome or "Consumidor Final", "tel": cliente_tel or None}).scalar()
                
                # 2. Buscar ou criar vendedor baseado no funcionário
                # Tenta encontrar vendedor com mesmo nome
                row = conn.execute(text("""
                    SELECT id FROM vendedores WHERE empresa_id = 1 AND nome = :nome AND ativo = TRUE LIMIT 1
                """), {"nome": funcionario_nome}).fetchone()
                
                if row:
                    vendedor_id = int(row[0])
                else:
                    # Cria vendedor baseado no funcionário
                    vendedor_id = conn.execute(text("""
                        INSERT INTO vendedores (empresa_id, nome, ativo)
                        VALUES (1, :nome, TRUE) RETURNING id
                    """), {"nome": funcionario_nome}).scalar()

            # Inserir venda e itens (transação principal)
            with engine.begin() as conn:
                venda_id = conn.execute(text("""
                    INSERT INTO vendas 
                    (empresa_id, cliente_id, vendedor_id, data_venda, total_bruto, total_desconto, total_liquido, total_custo, margem, status)
                    VALUES (1, :cli, :vend, CURRENT_DATE, :tb, :desc, :tl, :tc, :m, 'concluida')
                    RETURNING id
                """), {
                    "cli": cliente_id,
                    "vend": vendedor_id,
                    "tb": total_bruto_final,
                    "desc": desconto_final,
                    "tl": total_liquido_final,
                    "tc": total_custo_final,
                    "m": margem_final
                }).scalar()

                for it in itens_final:
                    conn.execute(text("""
                        INSERT INTO itens_venda 
                        (empresa_id, venda_id, produto_id, quantidade, preco_unitario, desconto, total_item, custo_unitario, margem_item)
                        VALUES (1, :vid, :pid, :qtd, :pu, :desc, :ti, :cu, :mi)
                    """), {
                        "vid": venda_id,
                        "pid": it["produto_id"],
                        "qtd": it["quantidade"],
                        "pu": it["preco_unitario"],
                        "desc": 0,  # desconto geral mantido na venda
                        "ti": it["subtotal"],
                        "cu": it["custo_unitario"],
                        "mi": it["subtotal"] - (it["quantidade"] * it["custo_unitario"])
                    })

            st.balloons()
            st.success(f"✅ Venda #{venda_id} registrada com sucesso!")
            st.info(f"👤 Cliente: {cliente_nome or 'Consumidor Final'} | 📱 {cliente_tel or '-'}")
            st.info(f"💰 Total: R$ {total_liquido_final:,.2f} | 💵 Margem: R$ {margem_final:,.2f}")
            st.rerun()

# =====================================================
# 5. IMPORTAR DADOS (COM SEGURANÇA E RESET)
# =====================================================
elif pagina == "📤 Importar Dados":
    st.title("📤 Importar Dados")
    
    aba_import, aba_export, aba_reset = st.tabs(["📤 Importar", "📥 Exportar", "⚠️ Zona de Perigo"])
    
    # ========== ABA IMPORTAR ==========
    with aba_import:
        st.subheader("Importar Dados de Planilhas")
        st.info("💡 Dica: Exporte primeiro para ver o formato esperado")
        
        # Inicializar estado de sessão para evitar duplicação
        if 'import_processado' not in st.session_state:
            st.session_state.import_processado = False
        if 'arquivo_processado' not in st.session_state:
            st.session_state.arquivo_processado = None
        
        tipo_import = st.selectbox("O que deseja importar?", ["Produtos", "Funcionários"])
        
        arquivo = st.file_uploader(
            f"Escolha o arquivo CSV/Excel",
            type=['csv', 'xlsx'],
            key="upload_import"
        )
        
        if arquivo and arquivo != st.session_state.arquivo_processado:
            try:
                # Ler arquivo
                if arquivo.name.endswith('.csv'):
                    df_upload = pd.read_csv(arquivo)
                else:
                    df_upload = pd.read_excel(arquivo)
                
                st.write(f"**Preview dos dados ({len(df_upload)} linhas):**")
                st.dataframe(df_upload.head(10), use_container_width=True)
                
                if st.button("✅ Confirmar Importação"):
                    with st.spinner("Importando dados..."):
                        count = 0
                        erros = []
                        
                        if tipo_import == "Produtos":
                            # Validar colunas mínimas
                            if 'nome' not in df_upload.columns or 'preco_venda' not in df_upload.columns:
                                st.error("❌ Arquivo deve ter pelo menos as colunas: nome, preco_venda")
                            else:
                                for idx, row in df_upload.iterrows():
                                    try:
                                        executar_sql("""
                                            INSERT INTO produtos (empresa_id, nome, codigo, categoria, preco_venda, preco_custo, ativo)
                                            VALUES (1, :nome, :codigo, :categoria, :venda, :custo, TRUE)
                                        """, {
                                            "nome": str(row['nome']),
                                            "codigo": str(row.get('codigo', '')),
                                            "categoria": str(row.get('categoria', 'Geral')),
                                            "venda": float(row['preco_venda']),
                                            "custo": float(row.get('preco_custo', 0))
                                        })
                                        count += 1
                                    except Exception as e:
                                        erros.append(f"Linha {idx+1}: {str(e)}")
                                
                                st.session_state.import_processado = True
                                st.session_state.arquivo_processado = arquivo
                                
                                if erros:
                                    st.warning(f"⚠️ {len(erros)} erro(s) encontrado(s)")
                                    for erro in erros[:5]:  # Mostrar apenas 5 primeiros
                                        st.text(erro)
                                
                                st.success(f"✅ {count} produto(s) importado(s) com sucesso!")
                                st.rerun()
                        
                        elif tipo_import == "Funcionários":
                            # Validar colunas mínimas
                            if 'nome' not in df_upload.columns:
                                st.error("❌ Arquivo deve ter pelo menos a coluna: nome")
                            else:
                                for idx, row in df_upload.iterrows():
                                    try:
                                        executar_sql("""
                                            INSERT INTO funcionarios (empresa_id, nome, cargo, ativo)
                                            VALUES (1, :nome, :cargo, TRUE)
                                        """, {
                                            "nome": str(row['nome']),
                                            "cargo": str(row.get('cargo', 'Vendedor'))
                                        })
                                        count += 1
                                    except Exception as e:
                                        erros.append(f"Linha {idx+1}: {str(e)}")
                                
                                st.session_state.import_processado = True
                                st.session_state.arquivo_processado = arquivo
                                
                                if erros:
                                    st.warning(f"⚠️ {len(erros)} erro(s) encontrado(s)")
                                    for erro in erros[:5]:
                                        st.text(erro)
                                
                                st.success(f"✅ {count} funcionário(s) importado(s) com sucesso!")
                                st.rerun()
            
            except Exception as e:
                st.error(f"❌ Erro ao processar arquivo: {str(e)}")
                st.info("Verifique se as colunas estão corretas e o formato do arquivo")
        
        # Botão para resetar estado de importação
        if st.session_state.import_processado:
            if st.button("🔄 Importar Novo Arquivo"):
                st.session_state.import_processado = False
                st.session_state.arquivo_processado = None
                st.rerun()
    
    # ========== ABA EXPORTAR ==========
    with aba_export:
        st.subheader("Exportar Dados para CSV")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Exportar Produtos**")
            df_produtos_exp = carregar_dados("SELECT * FROM produtos WHERE ativo = TRUE")
            if not df_produtos_exp.empty:
                csv_produtos = df_produtos_exp.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Baixar Produtos.csv",
                    data=csv_produtos,
                    file_name="produtos.csv",
                    mime="text/csv"
                )
            else:
                st.info("Nenhum produto cadastrado")
        
        with col2:
            st.markdown("**Exportar Vendas**")
            df_vendas_exp = carregar_dados("""
                SELECT 
                    v.id, v.data_venda, v.total_liquido, v.margem,
                    iv.produto_id, p.nome as produto, iv.quantidade, iv.preco_unitario
                FROM vendas v
                JOIN itens_venda iv ON v.id = iv.venda_id
                JOIN produtos p ON iv.produto_id = p.id
                ORDER BY v.data_venda DESC
            """)
            if not df_vendas_exp.empty:
                csv_vendas = df_vendas_exp.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Baixar Vendas.csv",
                    data=csv_vendas,
                    file_name="vendas.csv",
                    mime="text/csv"
                )
            else:
                st.info("Nenhuma venda registrada")
        
        st.divider()
        
        st.markdown("**Exportar Funcionários**")
        df_func_exp = carregar_dados("SELECT * FROM funcionarios WHERE ativo = TRUE")
        if not df_func_exp.empty:
            csv_func = df_func_exp.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Baixar Funcionarios.csv",
                data=csv_func,
                file_name="funcionarios.csv",
                mime="text/csv"
            )
        else:
            st.info("Nenhum funcionário cadastrado")
    
    # ========== ABA ZONA DE PERIGO ==========
    with aba_reset:
        st.subheader("⚠️ Zona de Perigo")
        st.warning("🚨 ATENÇÃO: Esta ação é IRREVERSÍVEL!")
        
        st.markdown("""
        **O que será feito:**
        - Todos os dados das tabelas serão apagados
        - Os IDs serão resetados (começarão do 1 novamente)
        - As tabelas NÃO serão apagadas (apenas os dados)
        
        **Tabelas afetadas:**
        - `produtos`
        - `vendas`
        - `itens_venda`
        - `funcionarios`
        """)
        
        confirmacao = st.text_input(
            "Digite 'RESETAR' para confirmar:",
            key="confirm_reset"
        )
        
        if confirmacao == "RESETAR":
            if st.button("🗑️ EXECUTAR RESET DO BANCO", type="primary"):
                with st.spinner("Resetando banco de dados..."):
                    try:
                        with engine.begin() as conn:
                            # Executar TRUNCATE com RESTART IDENTITY e CASCADE
                            conn.execute(text("""
                                TRUNCATE TABLE produtos, vendas, itens_venda, funcionarios 
                                RESTART IDENTITY CASCADE
                            """))
                        st.error("✅ Banco de dados resetado com sucesso!")
                        st.info("🔄 Recarregue a página para ver as mudanças")
                    except Exception as e:
                        st.error(f"❌ Erro ao resetar: {str(e)}")
        else:
            st.info("Digite 'RESETAR' no campo acima para habilitar o botão")
