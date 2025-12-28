import streamlit as st
import yt_dlp
import os

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Universal Video Downloader",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Universal Video Downloader")
st.write("Download com diagnóstico automático de proteção")

# ==============================
# INPUT
# ==============================
url = st.text_input("Cole a URL do vídeo aqui:")

# ==============================
# BOTÃO PRINCIPAL
# ==============================
if st.button("Analisar e Baixar"):
    if not url:
        st.warning("Insira um link válido.")
        st.stop()

    try:
        # ==============================
        # OPÇÕES DO yt-dlp (SEGURAS)
        # ==============================
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'merge_output_format': 'mp4',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        
            # 🔑 ESSENCIAL
            'cookiefile': 'cookies.txt',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.youtube.com/',
                'Accept-Language': 'pt-BR,pt;q=0.9',
            },
        }

        # ==============================
        # ETAPA 1 — ANÁLISE
        # ==============================
        with st.spinner("🔍 Analisando o conteúdo..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

        st.subheader("🔍 Diagnóstico do Conteúdo")
        st.write("**Extractor:**", info.get("extractor"))
        st.write("**Título:**", info.get("title"))
        st.write("**Site:**", info.get("webpage_url_domain"))
        st.write("**DRM declarado:**", info.get("drm", False))
        st.write("**É live:**", info.get("is_live", False))
        st.write("**Quantidade de formatos encontrados:**", len(info.get("formats", [])))

        # ==============================
        # BLOQUEIOS CONHECIDOS
        # ==============================
        if info.get("drm"):
            st.error("❌ Conteúdo protegido por DRM. Download não permitido.")
            st.stop()

        if not info.get("formats"):
            st.error("❌ Nenhum formato disponível. Possível bloqueio do site.")
            st.stop()

        st.success("✔️ Formatos acessíveis detectados (sem DRM)")

        # ==============================
        # ETAPA 2 — DOWNLOAD
        # ==============================
        with st.spinner("⬇️ Baixando o vídeo..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

        # ==============================
        # ETAPA 3 — LOCALIZAR ARQUIVO REAL
        # ==============================
        filename = None

        if "requested_downloads" in info:
            for d in info["requested_downloads"]:
                if d.get("filepath"):
                    filename = d["filepath"]
                    break

        if not filename:
            filename = info.get("_filename")

        # ==============================
        # VALIDAÇÃO FINAL
        # ==============================
        if not filename or not os.path.exists(filename):
            st.error("❌ O arquivo final não foi localizado.")
            st.stop()

        if os.path.getsize(filename) == 0:
            st.error("❌ O arquivo foi criado, mas está vazio.")
            st.stop()

        # ==============================
        # SUCESSO
        # ==============================
        st.success("✅ Download concluído com sucesso!")
        with open(filename, "rb") as f:
            st.download_button(
                "⬇️ Clique para salvar o vídeo",
                data=f,
                file_name=os.path.basename(filename),
                mime="video/mp4"
            )

    except yt_dlp.utils.DownloadError as e:
        st.error(f"❌ Erro do yt-dlp: {e}")

    except Exception as e:
        st.error(f"❌ Erro inesperado: {e}")
