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
            st.write("**É live:**", info.get("is_live", False))

            formats = info.get("formats", [])
            st.write("**Quantidade de formatos encontrados:**", len(formats))

            if not formats:
                st.error("❌ Nenhum formato disponível → bloqueio total do site.")
                st.stop()

            # 🔐 VERIFICA DRM OCULTO
            drm_formats = [f for f in formats if f.get("has_drm")]
            if drm_formats:
                st.error("❌ DRM detectado nos formatos. Download impossível.")
                st.stop()

            st.success("✔️ Formatos acessíveis detectados (sem DRM explícito)")

            # ⬇️ TENTATIVA DE DOWNLOAD
            with st.spinner("⬇️ Tentando baixar o vídeo..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

            # 🔎 VERIFICAÇÃO FINAL
            if not os.path.exists(filename):
                st.error("❌ Arquivo final NÃO foi criado.")
            elif os.path.getsize(filename) == 0:
                st.error(
                    "❌ Arquivo criado com 0 bytes.\n\n"
                    "📌 DIAGNÓSTICO CONFIRMADO:\n"
                    "- O site entrega resposta vazia propositalmente\n"
                    "- Bloqueio por sessão / cookies / token temporário\n"
                    "- Proteção anti-bot ativa\n"
                    "- Download só funciona com navegador autenticado\n\n"
                    "➡️ SOLUÇÃO: cookies do navegador (cookies.txt)"
                )
            else:
                st.success("✅ Download realizado com sucesso!")
                with open(filename, "rb") as f:
                    st.download_button(
                        "⬇️ Salvar vídeo",
                        data=f,
                        file_name=os.path.basename(filename),
                        mime="video/mp4"
                    )

            # 📜 LOG TÉCNICO
            st.subheader("🧾 Log técnico do yt-dlp")
            st.code(log_buffer.getvalue())

        except Exception as e:
            st.error("❌ Falha inesperada")
            st.code(str(e))
