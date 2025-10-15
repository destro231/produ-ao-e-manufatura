# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 13:49:01 2025

@author: LAB-13
"""

import streamlit as st 
import pandas as pd
st.title("produçao e manufatura ianes")
st.video('manofaturing.mp4')
# dadaos
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

if bt1:
   novo={'data':[novo_data],
        'maquina':[nova_maquina],
          'turno':[turnos],
          'peças':[int(peças)],
          'peças defeituosas':[int(pecd)]}
   x=pd.DataFrame(novo)
   df=pd.concat([df,x],ignore_index=True)
   st.dataframe(df)
   df.to_csv("C:/Users/LAB-13/Desktop/WPy64-31241/trabalho/Data user.csv",index=False)
DataMachine=st.file_uploader(' arquivo')
if DataMachine is not None:
    df=pd.read_csv(DataMachine)
else:
    df = []
st.dataframe(df)
Form= st.sidebar.form('entrada',clear_on_submit=True)
Form.header("Edite os dados da maquina:")

nova_data=Form.text_input("data: ")
novas_maquina=Form.text_input("maquina: ")
turno = Form.text_input("turno: ")
peças = Form.text_input("peças produzidas: ")
pec = Form.text_input("peças defeituosas: ")
bt2=Form.form_submit_button('enviar')

if bt2:
    edit={'data':[novo_data],
           'maquina':[nova_maquina],
           'turno':[turnos],
           'peças':[int(peças)],
           'peças defeituosas':[int(pecd)]}
    x=pd.DataFrame(edit)
    df=pd.concat([df,x],ignore_index=True)
    st.dataframe(df)
    df.to_csv("C:/Users/LAB-13/Desktop/WPy64-31241/trabalho/DADOS.csv",index=False)




