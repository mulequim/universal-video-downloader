import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Universal Downloader", page_icon="🚀")
st.title("🚀 Universal Video Downloader")

url = st.text_input("Cole a URL do vídeo aqui:")

if st.button("Preparar Download"):
    if url:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'video_final.%(ext)s',
                'noplaylist': True,
                'quiet': True,
            }

            with st.spinner('Baixando vídeo...'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                with open(filename, "rb") as f:
                    st.success("✅ Vídeo pronto!")
                    st.download_button(
                        "⬇️ Clique para salvar",
                        data=f,
                        file_name=os.path.basename(filename),
                        mime="video/mp4"
                    )
            else:
                st.error("❌ Arquivo gerado está vazio.")

        except Exception as e:
            st.error(f"Erro detalhado: {e}")
    else:
        st.warning("Insira um link.")
