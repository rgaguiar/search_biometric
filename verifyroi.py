import streamlit as st
import pandas as pd
import os
import shutil
from PIL import Image

def load_dataframe():
    df = pd.read_csv("df_imgpath.csv")
    df = df.dropna(subset=['Endereço_roi'])  # Filtrar apenas imagens com ROI
    return df

def move_images(selected_valid, df):
    valid_path = "roi_invalidos"
    os.makedirs(valid_path, exist_ok=True)
    
    for _, row in df.iterrows():
        roi_path = row['Endereço_roi']
        if roi_path in selected_valid and os.path.exists(roi_path):
            destino = os.path.join(valid_path, row['Pasta'])
            os.makedirs(destino, exist_ok=True)
            shutil.move(roi_path, os.path.join(destino, os.path.basename(roi_path)))
    
    st.success("Movimentação concluída!")

st.title("Palmprint: Validação de Imagens")

df = load_dataframe()

pastas_disponiveis = df['Pasta'].unique()
pasta_selecionada = st.selectbox("Selecione a pasta para análise:", pastas_disponiveis)

df_filtered = df[df['Pasta'] == pasta_selecionada]
selected_valid = []

for _, row in df_filtered.iterrows():
    col1, col2 = st.columns(2)
    with col1:
        st.image(Image.open(row['Endereço_img']), caption="Imagem Original", use_container_width=True)
    with col2:
        if os.path.exists(row['Endereço_roi']):
            st.image(Image.open(row['Endereço_roi']), caption="Imagem ROI", use_container_width=True)
        else:
            st.write("**ROI DESCARTADO**")
        if st.button(f"DESCARTAR ROI - {row['NomeArquivo']}"):
            selected_valid.append(row['Endereço_roi'])
            st.success(f"ROI {row['NomeArquivo']} DESCARTADO.")

if st.button("Salvar alterações"):
    move_images(selected_valid, df_filtered)