import streamlit as st  # Biblioteca para criar a interface web
import pandas as pd     # Biblioteca para trabalhar com dados em tabela
import matplotlib.pyplot as plt  # Biblioteca para criar gráficos

# 1. Carregar o arquivo CSV
st.title("App de Produção e Manufatura")  # Título do aplicativo

uploaded_file = st.file_uploader("DADOS.csv")  # Botão para upload do arquivo

if uploaded_file is not None:  # Se o usuário carregou um arquivo
    df = pd.read_csv(uploaded_file)  # Lê o arquivo e armazena na variável df
else:  # Se não carregou, cria uma tabela vazia
    df = pd.DataFrame(columns=['Data', 'Máquina', 'Turno', 'Peças Produzidas', 'Peças Defeituosas'])
    st.write("Nenhum arquivo carregado. Crie novos dados.")

# Adiciona colunas calculadas se não existirem (para eficiência)
if 'Peças Boas' not in df.columns:
    df['Peças Boas'] = df['Peças Produzidas'] - df['Peças Defeituosas']  # Calcula peças boas
if 'Eficiência (%)' not in df.columns:
    df['Eficiência (%)'] = (df['Peças Boas'] / df['Peças Produzidas']) * 100  # Calcula eficiência
    df['Eficiência (%)'] = df['Eficiência (%)'].fillna(0)  # Evita erros se divisão por zero

st.dataframe(df)  # Exibe a tabela

# 2. Formulário para adicionar novos registros
with st.sidebar.form("adicionar_dados"):  # Formulário no sidebar para adicionar
    st.header("Adicionar Novo Registro")
    nova_data = st.text_input("Data (ex: 2025-10-10)")
    nova_maquina = st.text_input("Máquina (ex: M1)")
    novo_turno = st.text_input("Turno (ex: Manhã)")
    novas_pecas = st.text_input("Peças Produzidas")
    novas_pecas_defeituosas = st.text_input("Peças Defeituosas")
    
    submit_add = st.form_submit_button("Adicionar")
    
    if submit_add:  # Se o botão for clicado
        nova_linha = {
            'Data': nova_data,
            'Máquina': nova_maquina,
            'Turno': novo_turno,
            'Peças Produzidas': int(novas_pecas) if novas_pecas.isdigit() else 0,
            'Peças Defeituosas': int(novas_pecas_defeituosas) if novas_pecas_defeituosas.isdigit() else 0
        }
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)  # Adiciona a nova linha
        df['Peças Boas'] = df['Peças Produzidas'] - df['Peças Defeituosas']  # Recalcula peças boas
        df['Eficiência (%)'] = (df['Peças Boas'] / df['Peças Produzidas']) * 100  # Recalcula eficiência
        st.success("Registro adicionado!")

# 3. Formulário para editar registros (simples, baseado na data)
with st.sidebar.form("editar_dados"):
    st.header("Editar Registro")
    data_to_edit = st.text_input("Data para editar (ex: 2025-10-10)")
    nova_maquina_edit = st.text_input("Nova Máquina")
    novo_turno_edit = st.text_input("Novo Turno")
    novas_pecas_edit = st.text_input("Novas Peças Produzidas")
    novas_pecas_defeituosas_edit = st.text_input("Novas Peças Defeituosas")
    
    submit_edit = st.form_submit_button("Atualizar")
    
    if submit_edit:  # Se o botão for clicado
        if data_to_edit in df['Data'].values:  # Verifica se a data existe
            indice = df[df['Data'] == data_to_edit].index[0]  # Pega o primeiro índice
            df.at[indice, 'Máquina'] = nova_maquina_edit
            df.at[indice, 'Turno'] = novo_turno_edit
            df.at[indice, 'Peças Produzidas'] = int(novas_pecas_edit)
            if novas_pecas_edit.isdigit() :
                df.at[indice, 'Peças Produzidas'] = int(novas_pecas_edit)
            else :
                df.at[indice, 'Peças Produzidas'] = df.at[indice, 'Peças Produzidas']
            df.at[indice, 'Peças Defeituosas'] = int(novas_pecas_defeituosas_edit)
            if novas_pecas_defeituosas_edit.isdigit():
                df.at[indice, 'Peças Defeituosas'] = int(novas_pecas_defeituosas_edit)
            else:
                df.at[indice, 'Peças Defeituosas'] = df.at[indice, 'Peças Defeituosas']
            df['Peças Boas'] = df['Peças Produzidas'] - df['Peças Defeituosas']  # Recalcula
            df['Eficiência (%)'] = (df['Peças Boas'] / df['Peças Produzidas']) * 100  # Recalcula
            st.success("Registro editado!")
        else:
            st.error("Data não encontrada.")

# 4. Filtros interativos
st.header("Filtros")
data_inicio = st.date_input("Data de início")
data_fim = st.date_input("Data de fim")
maquina_selecionada = st.selectbox("Selecione uma máquina", options=['Todas'] + list(df['Máquina'].unique()))
turno_selecionado = st.selectbox("Selecione um turno", options=['Todos'] + list(df['Turno'].unique()))

df_filtrado = df.copy()  # Cria uma cópia para filtrar

# Aplica filtros
df_filtrado = df_filtrado[(df_filtrado['Data'] >= str(data_inicio)) & (df_filtrado['Data'] <= str(data_fim))]
if maquina_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Máquina'] == maquina_selecionada]
if turno_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Turno'] == turno_selecionado]

# 5. Gráficos interativos
st.header("Gráficos")
if not df_filtrado.empty:  # Só cria gráficos se houver dados
    # Gráfico 1: Produção diária por máquina
    producao_diaria = df_filtrado.groupby(['Data', 'Máquina'])['Peças Produzidas'].sum().unstack()
    plt.figure(figsize=(8, 4))
    producao_diaria.plot(kind='bar', ax=plt.gca())
    plt.title("Produção Diária por Máquina")
    plt.xlabel("Data")
    plt.ylabel("Peças Produzidas")
    st.pyplot(plt)  # Exibe o gráfico no Streamlit
    
    # Gráfico 2: Taxa de defeitos
    df_filtrado['Taxa de Defeitos (%)'] = (df_filtrado['Peças Defeituosas'] / df_filtrado['Peças Produzidas']) * 100
    taxa_defeitos = df_filtrado.groupby('Máquina')['Taxa de Defeitos (%)'].mean()
    plt.figure(figsize=(8, 4))
    taxa_defeitos.plot(kind='bar')
    plt.title("Taxa de Defeitos por Máquina")
    plt.ylabel("Taxa de Defeitos (%)")
    st.pyplot(plt)  # Exibe o gráfico

# 6. Cálculo e exibição de métricas
st.header("Métricas de Eficiência")
if not df_filtrado.empty:
    eficiencia_diaria = df_filtrado['Eficiência (%)'].mean()  # Média de eficiência
    media_producao = df_filtrado.groupby('Máquina')['Peças Produzidas'].mean()  # Média de produção por máquina
    st.write(f"Média de Eficiência Diária: {eficiencia_diaria:.2f}%")
    st.write("Média de Produção por Máquina:")
    st.write(media_producao)
    
    # 7. Alertas automáticos
    if eficiencia_diaria < 90:  # Alerta se eficiência < 90%
        st.error("Alerta: Eficiência diária abaixo de 90%!")
    for maquina in df_filtrado['Máquina'].unique():
        if df_filtrado[df_filtrado['Máquina'] == maquina]['Peças Produzidas'].sum() < 80:  # Alerta se produção < 80 peças/dia
            st.error(f"Alerta: Produção da máquina {maquina} abaixo de 80 peças!")

# 8. Botão para salvar os dados atualizados
if st.button("Salvar Dados Atualizados"):
    df.to_csv("DADOS.csv", index=False)  # Salva em um novo arquivo
    st.success("Dados salvos em 'dados_atualizados.csv'!")








