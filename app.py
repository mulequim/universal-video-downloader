import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Universal Downloader", page_icon="🚀")

st.title("🚀 Universal Video Downloader")

url = st.text_input("Cole a URL do vídeo aqui:")

if st.button("Preparar Download"):
    if url:
        try:
            # Opções otimizadas para evitar bloqueios e arquivos vazios
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video_baixado.%(ext)s',
                'noplaylist': True,
                # O User-Agent ajuda a evitar o erro de "file is empty"
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }

            with st.spinner('Baixando vídeo... Isso pode levar alguns segundos.'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                
                with open(filename, "rb") as file:
                    st.success("✅ Vídeo processado com sucesso!")
                    st.download_button(
                        label="Clique aqui para salvar o vídeo",
                        data=file,
                        file_name=os.path.basename(filename),
                        mime="video/mp4"
                    )
        except Exception as e:
            st.error(f"Erro detalhado: {e}")
    else:
        st.warning("Insira um link válido.")
