import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Universal Downloader", page_icon="🚀")
st.title("🚀 Universal Video Downloader (Diagnóstico Ativo)")

url = st.text_input("Cole a URL do vídeo aqui:")

if st.button("Analisar e Baixar"):
    if not url:
        st.warning("Insira um link.")
    else:
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'video_final.%(ext)s',
                'noplaylist': True,
                'quiet': True,
                'nocheckcertificate': True,
            }

            with st.spinner("🔍 Analisando vídeo..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)

            # 🔍 DIAGNÓSTICO 1 — DRM
            if info.get("drm"):
                st.error("❌ Este vídeo possui DRM. Download não é possível.")
                st.stop()

            # 🔍 DIAGNÓSTICO 2 — Sem formatos válidos
            formats = info.get("formats", [])
            if not formats:
                st.error("❌ Nenhum formato disponível. Possível bloqueio do site.")
                st.stop()

            # 🔍 DIAGNÓSTICO 3 — Requer login
            extractor = info.get("extractor", "").lower()
            if extractor in ["instagram", "facebook", "tiktok"]:
                st.warning(
                    "⚠️ Este site normalmente exige login.\n"
                    "➡️ Se falhar, use cookies do navegador."
                )

            # ⬇️ DOWNLOAD REAL
            with st.spinner("⬇️ Baixando vídeo..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

            # 🔍 DIAGNÓSTICO 4 — Arquivo vazio
            if not os.path.exists(filename):
                st.error("❌ O arquivo final não foi criado.")
                st.stop()

            if os.path.getsize(filename) == 0:
                st.error(
                    "❌ O arquivo foi criado, mas está vazio.\n\n"
                    "📌 Possíveis causas:\n"
                    "- Site bloqueou o download\n"
                    "- Conteúdo exige cookies/login\n"
                    "- Stream protegido\n"
                    "- Link não aponta para o vídeo real"
                )
                st.stop()

            # ✅ SUCESSO
            with open(filename, "rb") as f:
                st.success("✅ Vídeo baixado com sucesso!")
                st.download_button(
                    "⬇️ Clique para salvar",
                    data=f,
                    file_name=os.path.basename(filename),
                    mime="video/mp4"
                )

        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e).lower()

            if "drm" in error_msg:
                st.error("❌ DRM detectado. Download não permitido.")
            elif "login" in error_msg or "cookies" in error_msg:
                st.error("🔐 O site exige login. Use cookies do navegador.")
            elif "403" in error_msg:
                st.error("🚫 Erro 403: acesso bloqueado pelo site.")
            elif "unsupported url" in error_msg:
                st.error("❌ URL não suportada pelo yt-dlp.")
            else:
                st.error(f"❌ Erro do yt-dlp: {e}")

        except Exception as e:
            st.error(f"❌ Erro inesperado: {e}")
