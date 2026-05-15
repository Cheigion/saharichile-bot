import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# ─── CONFIGURACION ───────────────────────────────────────────────────────────
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8834944319:AAFK31NqLANHQpqD-grYZ_W81yuLpBFB2xE")
ADMIN_CHAT_ID = 8514619938

MENU = """
🍱 <b>Nuestros productos:</b>

🔹 <b>HandRoll</b> - $1.200
🔹 <b>Sopaipilla</b> - $300

📍 <b>Ubicación:</b> Santiago 345, La Pintana

¡Te esperamos! 😊
"""

BIENVENIDA = """
👋 ¡Hola! Bienvenido a <b>SahariChile</b> 🍱

Puedes preguntarme por:
🔹 Nuestros <b>precios</b>
🔹 Nuestro <b>menú</b>
🔹 Nuestra <b>ubicación</b>

¡Con gusto te ayudo! 😊
"""

# Palabras clave que el bot sabe responder
PALABRAS_MENU = [
    "handroll", "hand roll", "sopaipilla", "precio", "precios",
    "cuanto", "cuánto", "vale", "cuesta", "menu", "menú", "carta",
    "ubicacion", "ubicación", "donde", "dónde", "direccion", "dirección",
    "local", "lugar"
]

# ─── HANDLERS ────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /start"""
    await update.message.reply_text(BIENVENIDA, parse_mode="HTML")


async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja todos los mensajes de texto"""
    mensaje = update.message.text.lower()
    chat_id = update.message.chat_id
    nombre = update.message.from_user.first_name or "Cliente"
    mensaje_original = update.message.text

    # Verificar si el bot sabe responder
    sabe_responder = any(palabra in mensaje for palabra in PALABRAS_MENU)

    if sabe_responder:
        # Responder con precios y ubicacion
        await update.message.reply_text(MENU, parse_mode="HTML")
    else:
        # Avisar al cliente
        await update.message.reply_text(
            "🤖 Lo voy a consultar con el administrador y te respondo pronto. ¡Gracias por tu paciencia! 😊"
        )

        # Notificar al admin
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"⚠️ <b>Consulta de cliente</b>\n\n👤 <b>Cliente:</b> {nombre}\n💬 <b>Preguntó:</b> {mensaje_original}\n\n📌 Por favor respóndele en @saharichile_bot",
            parse_mode="HTML"
        )


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))

    print("🤖 SahariChile Bot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    main()
