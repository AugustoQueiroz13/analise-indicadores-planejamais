import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Planeja+", layout="wide")
st.title("Análise de Indicadores - Programa Planeja+")

# 1. CARREGAMENTO DOS DADOS
df_atividades = pd.read_excel('atividades.xlsx', header=1)
df_metas = pd.read_excel('metas.xlsx')

# 2. TRATAMENTO E LIMPEZA DE DADOS 
# Removendo registros duplicados
df_atividades = df_atividades.drop_duplicates()

# Padronizando a coluna de Municípios 
if 'Município' in df_atividades.columns:
    df_atividades['Município'] = df_atividades['Município'].astype(str).str.upper().str.strip()

# Convertendo datas e tratando erros 
df_atividades['Data realizada'] = pd.to_datetime(df_atividades['Data realizada'], errors='coerce')


# 3. CONSTRUÇÃO DO DASHBOARD
aba1, aba2 = st.tabs(["Atividade 1: Métricas Gerais", "Atividade 2: Transparência Guapimirim"])

with aba1:
    st.header("Visão Exploratória e Acompanhamento de Metas")
    
    # Métrica 1: Total de Atividades válidas
    total_atividades = len(df_atividades)
    
    # Métrica 2: Média Mensal
    df_atividades['Mes'] = df_atividades['Data realizada'].dt.month
    meses_unicos = df_atividades['Mes'].dropna().nunique()
    media_mensal = total_atividades / meses_unicos if meses_unicos > 0 else 0
    
    # Métrica 3: 
    urgencia = df_atividades[df_atividades['Data prevista'] == 'Atividade não prevista'].shape[0]
    
    # Exibindo os cards superiores
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Atividades (Sem Duplicatas)", total_atividades)
    col2.metric("Média Mensal de Atividades", round(media_mensal, 2))
    col3.metric("Ações Não Previstas", urgencia)
    
    st.divider()
    
    col_grafico1, col_grafico2 = st.columns(2)
    
    with col_grafico1:
        # Métrica 4: Engajamento por Município
        st.subheader("Participantes por Município (Dados Padronizados)")
        engajamento = df_atividades.groupby('Município')['Número de participantes'].sum().reset_index()
        fig_engajamento = px.pie(engajamento, values='Número de participantes', names='Município', hole=0.4)
        st.plotly_chart(fig_engajamento, use_container_width=True)
        
    with col_grafico2:
        # Métrica 5: 
        st.subheader("Top Atividades em Volume de Público")
        top3 = df_atividades.groupby('Atividade')['Número de participantes'].sum().nlargest(3).reset_index()
        fig_top3 = px.bar(top3, x='Atividade', y='Número de participantes', text='Número de participantes', color='Atividade')
        st.plotly_chart(fig_top3, use_container_width=True)

    st.divider()
    
    # Métrica 6: Acompanhamento de Metas
    st.subheader("Acompanhamento de Metas (Realizado vs Previsto)")
    realizado = df_atividades.groupby('Atividade').size().reset_index(name='Realizado')
    metas_df = df_metas.rename(columns={'Atividades': 'Atividade'})
    progresso = pd.merge(metas_df, realizado, on='Atividade', how='left').fillna(0)
    progresso['% Concluído'] = (progresso['Realizado'] / progresso['Meta']) * 100
    
    fig_progresso = px.bar(progresso.nlargest(5, 'Realizado'), x='Atividade', y=['Realizado', 'Meta'], barmode='group')
    st.plotly_chart(fig_progresso, use_container_width=True)

with aba2:
    st.header("Levantamento Orçamentário - Município de Guapimirim")
    st.write("Análise da dependência de rendas petrolíferas no orçamento municipal.")
    
    # 1. VALORES BRUTOS  
    receita_bruta = 229678882.00 
    despesa_bruta = 22028173.27
    royalties_brutos = 2978642.32
    
    # 2.  ESCALA E PORCENTAGEM
    receita_escala = receita_bruta / 1000000
    despesa_escala = despesa_bruta / 1000000
    royalties_escala = royalties_brutos / 1000000
    pct_royalties = (royalties_brutos / receita_bruta) * 100 if receita_bruta > 0 else 0
    
    # 3. TABELA FORMATADA
    dados_guapi = {
        "Ano": ["2023", "2023", "2023", "2023"],
        "Indicador": ["Receita Total", "Despesa Total", "Receita de Royalties", "% Royalties na Receita"],
        "Valor": [
            f"R$ {receita_escala:.2f} Milhões", 
            f"R$ {despesa_escala:.2f} Milhões", 
            f"R$ {royalties_escala:.2f} Milhões", 
            f"{pct_royalties:.2f} %"
        ] 
    }
    st.table(pd.DataFrame(dados_guapi))
    
    st.markdown("""
    ### Processo de Tratamento e Metodologia (Atividade 2)
    * **Padronização e Escala:** Os valores financeiros originais foram convertidos internamente no script para a escala de milhões. Esta técnica evita a poluição visual da tabela, garantindo uma leitura direta para a tomada de decisão.
    * **Nota Técnica sobre Coleta de Dados:** O projeto previu inicialmente a extração automatizada via Web Scraping com Python e Selenium. No entanto, o Portal da Transparência de Guapimirim utiliza um firewall com verificação anti-bot ativa, que bloqueia requisições automatizadas. Para garantir a precisão e a entrega dentro do escopo do teste, a amostra financeira foi consolidada de forma estática no script, mantendo o cálculo relacional dinâmico.
    """)
