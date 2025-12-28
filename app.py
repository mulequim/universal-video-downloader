import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Universal Downloader", page_icon="🚀")
st.title("🚀 Universal Video Downloader")

url = st.text_input("Cole a URL do vídeo aqui:")

if st.button("Preparar Download"):
    if not url:
        st.warning("Insira um link.")
    else:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'video_final.%(ext)s',
                'noplaylist': True,
                'quiet': True,
            }

            with st.spinner("Baixando vídeo..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

            # 🔒 VERIFICAÇÃO CRÍTICA
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                st.error("❌ O arquivo foi gerado vazio. O site pode bloquear downloads.")
            else:
                with open(filename, "rb") as f:
                    st.success("✅ Vídeo pronto!")
                    st.download_button(
                        "⬇️ Clique para salvar",
                        data=f,
                        file_name=os.path.basename(filename),
                        mime="video/mp4"
                    )

        except Exception as e:
            st.error(f"Erro detalhado: {e}")
