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

¿Quieres saber dónde estamos? ¡Pregúntame por nuestra ubicación! 📍
"""

UBICACION = """
📍 <b>Nuestra ubicación:</b>

Santiago 345, La Pintana

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

# Palabras clave para precios
PALABRAS_PRECIOS = [
    "handroll", "hand roll", "sopaipilla", "precio", "precios",
    "cuanto", "cuánto", "vale", "cuesta", "menu", "menú", "carta"
]

# Palabras clave para ubicación
PALABRAS_UBICACION = [
    "ubicacion", "ubicación", "donde", "dónde", "direccion", "dirección",
    "local", "lugar", "queda", "quedan"
]

# Palabras de saludo
PALABRAS_SALUDO = [
    "hola", "buenas", "buen dia", "buenos dias", "hi", "ola", "hello", "start"
]

# ─── HANDLERS ────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /start"""
    await update.message.reply_text(BIENVENIDA, parse_mode="HTML")


async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja todos los mensajes de texto"""
    mensaje = update.message.text.lower()
    nombre = update.message.from_user.first_name or "Cliente"
    mensaje_original = update.message.text

    es_saludo = any(palabra in mensaje for palabra in PALABRAS_SALUDO)
    es_precio = any(palabra in mensaje for palabra in PALABRAS_PRECIOS)
    es_ubicacion = any(palabra in mensaje for palabra in PALABRAS_UBICACION)

    if es_saludo:
        await update.message.reply_text(BIENVENIDA, parse_mode="HTML")

    elif es_precio:
        await update.message.reply_text(MENU, parse_mode="HTML")

    elif es_ubicacion:
        await update.message.reply_text(UBICACION, parse_mode="HTML")

    else:
        await update.message.reply_text(
            "🤖 Lo voy a consultar con el administrador y te respondo pronto. ¡Gracias por tu paciencia! 😊"
        )
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"⚠️ <b>Consulta de cliente</b>\n\n👤 <b>Cliente:</b> {nombre}\n💬 <b>Preguntó:</b> {mensaje_original}\n\n📌 Por favor respóndele en @saharichile_bot",
            parse_mode="HTML"
        )


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    print("🤖 SahariChile Bot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    main()
