import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token de tu bot (obtenido de @BotFather)
TOKEN = "7604591073:AAF_0qkHnsnmv7_5fkUMOO55U2IZGtCBwVw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mensaje de bienvenida"""
    await update.message.reply_text(
        "¡Hola! Soy un bot para descargar videos de YouTube. 🎬\n"
        "Envíame un enlace y te lo descargaré.\n"
        "Usa /mp3 para descargar solo audio. 🎵\n\n"
        "Creado por: @martinc011"
    )

async def descargar_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga un video en MP4"""
    url = update.message.text
    try:
        await update.message.reply_text("📥 Descargando video...")
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': '%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        # Enviar el video
        await update.message.reply_video(video=open(filename, 'rb'))
        # Dar créditos
        await update.message.reply_text("✅ ¡Video descargado!\n\nCreado por: @martinc011 🚀")
        
        os.remove(filename)  # Eliminar el archivo después de enviar
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def descargar_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descarga solo audio en MP3"""
    url = update.message.text.replace("/mp3", "").strip()
    try:
        await update.message.reply_text("🎵 Descargando audio...")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        
        # Enviar el audio
        await update.message.reply_audio(audio=open(filename, 'rb'))
        # Dar créditos
        await update.message.reply_text("✅ ¡Audio descargado!\n\nCreado por: @falopeadito 🎧")
        
        os.remove(filename)  # Eliminar el archivo después de enviar
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    """Iniciar el bot"""
    app = Application.builder().token(TOKEN).build()
    
    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mp3", descargar_mp3))
    
    # Manejar mensajes con URLs
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, descargar_video))
    
    # Iniciar el bot
    app.run_polling()

if __name__ == "__main__":
    main()