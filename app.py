import streamlit as st
import yt_dlp
import os
import io
import contextlib

st.set_page_config(page_title="Universal Downloader", page_icon="🚀")
st.title("🚀 Universal Video Downloader — Diagnóstico Profundo")

url = st.text_input("Cole a URL do vídeo aqui:")

if st.button("Analisar Proteção"):
    if not url:
        st.warning("Insira um link.")
    else:
        log_buffer = io.StringIO()

        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'video_final.%(ext)s',
                'noplaylist': True,
                'quiet': True,
                'verbose': True,          # 🔥 DEBUG ATIVO
                'nocheckcertificate': True,
            }

            # 🔍 CAPTURA LOG INTERNO DO yt-dlp
            with contextlib.redirect_stdout(log_buffer), contextlib.redirect_stderr(log_buffer):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)

            # 📊 DIAGNÓSTICO ESTRUTURAL
            st.subheader("🔍 Diagnóstico do Conteúdo")

            st.write("**Extractor:**", info.get("extractor"))
            st.write("**Título:**", info.get("title"))
            st.write("**Site:**", info.get("webpage_url_domain"))
            st.write("**DRM declarado:**", info.get("drm", False))
            s
