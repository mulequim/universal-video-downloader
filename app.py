import streamlit as st
import yt_dlp
import os

# Configuração da página
st.set_page_config(page_title="Universal Downloader", page_icon="🚀")

st.title("🚀 Universal Video Downloader")
st.markdown("""
Baixe vídeos do **YouTube, Instagram, Facebook, TikTok** e muito mais. 
Basta colar o link abaixo!
""")

# Campo de entrada da URL
url = st.text_input("Cole a URL do vídeo aqui:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Preparar Download"):
    if not url:
        st.warning("Por favor, insira um link antes de continuar.")
    else:
        try:
            # Opções do yt-dlp
            # 'outtmpl': 'downloaded_video.%(ext)s' define o nome do arquivo temporário
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloaded_video.%(ext)s',
                'noplaylist': True,
            }

            with st.spinner('Extraindo informações do vídeo...'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Extrair info e baixar
                    info = ydl.extract_info(url, download=True)
                    video_filename = ydl.prepare_filename(info)
                    video_title = info.get('title', 'video_baixado')

                # Abrir o arquivo baixado para enviar ao usuário
                with open(video_filename, "rb") as file:
                    st.success(f"✅ Vídeo encontrado: **{video_title}**")
                    
                    st.download_button(
                        label="⬇️ Baixar Arquivo Agora",
                        data=file,
                        file_name=f"{video_title}.mp4",
                        mime="video/mp4"
                    )
            
            # Limpeza opcional: deletar o arquivo do servidor após carregar no botão
            # os.remove(video_filename)

        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o link: {str(e)}")
            st.info("Dica: Alguns vídeos do Instagram e YouTube podem exigir cookies se forem privados ou restritos.")

st.markdown("---")
st.caption("Criado com Python, Streamlit e yt-dlp.")
