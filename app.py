import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Universal Downloader", page_icon="🚀")
st.title("🚀 Universal Video Downloader")

url = st.text_input("Cole a URL do vídeo aqui:")

if st.button("Preparar Download"):
    if url:
        try:
            # Opções avançadas para contornar bloqueios
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': 'video_final.%(ext)s',
                'noplaylist': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                },
                'nocheckcertificate': True,
            }

            with st.spinner('Baixando... Isso pode demorar dependendo do tamanho do vídeo.'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                
                with open(filename, "rb") as file:
                    st.success("✅ Vídeo pronto!")
                    st.download_button(
                        label="Clique para Salvar",
                        data=file,
                        file_name=os.path.basename(filename),
                        mime="video/mp4"
                    )
        except Exception as e:
            st.error(f"Erro detalhado: {e}")
    else:
        st.warning("Insira um link.")
