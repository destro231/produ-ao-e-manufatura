import streamlit as st 
import pandas as pd
st.title("produçao e manufatura ianes")
st.markdown('''
            <style>
            .custom-font{
            font-family: 'Blippo', fantasy
            font-size: 60px;
            color: white;
            }
            </style>
            ''', unsafe_allow_html=True)
st.video('manofaturing.mp4')
# dados
Dados=st.file_uploader('carregar arquivo')
if Dados is not None:
    df=pd.read_csv(Dados)
else:
    df=[]
st.dataframe(df)
Formulario=st.sidebar.form('novas entradas',clear_on_submit=True)
Formulario.header("digite os novos dados da maquina:")
novo_data=Formulario.text_input("data: ")
nova_maquina=Formulario.text_input("maquina: ")
turnos = Formulario.text_input("turno: ")
peças = Formulario.text_input("peças produzidas: ")
pecd = Formulario.text_input("peças defeituosas: ")
bt1=Formulario.form_submit_button('enviar')

st.markdown('-'*20)

if bt1:
   novo={'data':[novo_data],
        'maquina':[nova_maquina],
          'turno':[turnos],
          'peças':[int(peças)],
          'peças defeituosas':[int(pecd)]}
   x=pd.DataFrame(novo)
   df=pd.concat([df,x],ignore_index=True)
   st.dataframe(df)
   df.to_csv("Data user.csv",index=False)
#//////////////////////////////////////////////////////////////////////////////////////
form = st.sidebar.form('entrada',clear_on_submit=True)
DataMachine=st.file_uploader(' arquivo')# nome do upload
try:
    if DataMachine is not None: 
        df_arquivo=pd.read_csv(DataMachine)
    else:
        df_arquivo = pd.DataFrame()
    
# Form= st.sidebar.form('entrada',clear_on_submit=True)#side bar
# Form.header("Edite os dados da maquina:")

# nova_data=Form.text_input("data: ")
# novas_maquina=Form.text_input("maquina: ")
# turno = Form.text_input("turno: ")
# peças = Form.text_input("peças produzidas: ")
# pec = Form.text_input("peças defeituosas: ")
    editar_df= form.data_editor(df)
    bt2=form.form_submit_button(' salvar')
   
    
#botao 2 novos dados

    if bt2:
       if not isinstance(df,pd.DataFrame):
           df=pd.DataFrame()
    
       df=pd.concat([df,editar_df],ignore_index=True)
    form.data_editor(df)
    df.to_csv("DADOS.csv",index=False)
except OSError:
    form.warning("diretorio inexistente")
except AttributeError:
    form.warning("sem arquivo")
#/////////////////////////////////////////////////////////////////////





