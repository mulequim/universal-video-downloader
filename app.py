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
st.write("Download direto usando sessão do Chrome (anti-bot do YouTube)")

# ==============================
# INPUT
# ==============================
url = st.text_input("Cole a URL do vídeo do YouTube:")

# ==============================
# BOTÃO
# ==============================
if st.button("Analisar e Baixar"):
    if not url:
        st.warning("⚠️ Cole um link válido.")
        st.stop()

    try:
        # ==============================
        # OPÇÕES yt-dlp (FUNCIONAIS)
        # ==============================
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": "%(title)s.%(ext)s",
            "noplaylist": True,
            "quiet": False,

            # 🔑 ESSENCIAL (ANTI-BOT)
            "cookiesfrombrowser": ("chrome",),
        }

        # ==============================
        # ETAPA 1 — ANÁLISE
        # ==============================
        with st.spinner("🔍 Analisando o vídeo..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

        st.subheader("🔍 Diagnóstico")
        st.write("**Título:**", info.get("title"))
        st.write("**Canal:**", info.get("uploader"))
        st.write("**É live:**", info.get("is_live"))
        st.write("**DRM:**", info.get("drm", False))
        st.write("**Formatos encontrados:**", len(info.get("formats", [])))

        if info.get("drm"):
            st.error("❌ Conteúdo com DRM. Não é possível baixar.")
            st.stop()

        st.success("✅ Vídeo liberado para download")

        # ==============================
        # ETAPA 2 — DOWNLOAD
        # ==============================
        with st.spinner("⬇️ Baixando o vídeo..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

        # ==============================
        # LOCALIZAR ARQUIVO
        # ==============================
        filename = info.get("_filename")

        if not filename or not os.path.exists(filename):
            st.error("❌ Arquivo não encontrado.")
            st.stop()

        if os.path.getsize(filename) == 0:
            st.error("❌ Arquivo vazio (bloqueio do YouTube).")
            st.stop()

        # ==============================
        # SUCESSO
        # ==============================
        st.success("✅ Download concluído com sucesso!")
        with open(filename, "rb") as f:
            st.download_button(
                label
