import os
import schedule
import time
import asyncio
import threading
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN   = os.environ.get("TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))

# ── Horario semanal ──
horario = {
    "Monday": [
        ("📐 Matemáticas", "Funciones en Khan Academy", "30 min"),
        ("🐍 Python",      "Variables y tipos de datos", "30 min"),
        ("🐧 Linux",       "Comandos básicos en terminal", "30 min"),
    ],
    "Tuesday": [
        ("⚡ Electricidad", "Ley de Ohm en Falstad", "45 min"),
        ("🐍 Python",       "Condicionales y bucles", "45 min"),
    ],
    "Wednesday": [
        ("📐 Matemáticas", "Trigonometría", "45 min"),
        ("🌿 Git",         "Subir ejercicios a GitHub", "45 min"),
    ],
    "Thursday": [
        ("⚡ Electricidad", "Kirchhoff KVL y KCL", "45 min"),
        ("🐍 Python",       "Funciones propias", "45 min"),
    ],
    "Friday": [
        ("🔗 Proyecto",    "Calculadora RL en Python", "90 min"),
    ],
    "Saturday": [
        ("📐 Matemáticas", "Logaritmos", "60 min"),
        ("📐 Matemáticas", "Números complejos", "60 min"),
    ],
    "Sunday": [
        ("📝 Repaso",      "Técnica Feynman", "45 min"),
    ],
}

dias_es = {
    "Monday":"Lunes", "Tuesday":"Martes", "Wednesday":"Miércoles",
    "Thursday":"Jueves", "Friday":"Viernes", "Saturday":"Sábado", "Sunday":"Domingo"
}

temas_completados = []
app = None

def construir_mensaje_hoy():
    dia = datetime.now().strftime("%A")
    if dia not in horario:
        return "No hay temas programados para hoy."
    mensaje = f"🗓 *{dias_es[dia]}* — Tu plan de hoy:\n\n"
    for tema, descripcion, tiempo in horario[dia]:
        completado = "✅" if tema in temas_completados else "⬜"
        mensaje += f"{completado} {tema}: {descripcion} — _{tiempo}_\n"
    mensaje += "\n💪 ¡Tú puedes! Un día a la vez."
    return mensaje

# ── Comandos ──
async def comando_hoy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = construir_mensaje_hoy()
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def comando_listo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /listo nombre del tema\nEjemplo: /listo Matemáticas")
        return

    tema_input = " ".join(context.args).lower()
    encontrado = None
    dia = datetime.now().strftime("%A")

    if dia in horario:
        for tema, _, _ in horario[dia]:
            if tema_input in tema.lower():
                encontrado = tema
                break

    if encontrado:
        if encontrado not in temas_completados:
            temas_completados.append(encontrado)
            await update.message.reply_text(f"✅ *{encontrado}* marcado como completado. ¡Excelente!", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"Ya habías completado *{encontrado}* hoy. 💪", parse_mode="Markdown")
    else:
        await update.message.reply_text("No encontré ese tema. Escribe /hoy para ver los temas de hoy.")

# ── Recordatorio automático (corre en hilo separado) ──
def enviar_recordatorio_sync():
    async def _enviar():
        temas_completados.clear()
        mensaje = construir_mensaje_hoy()
        async with Bot(token=TOKEN) as b:
            await b.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown")
        print("✅ Recordatorio enviado")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_enviar())
    loop.close()

def hilo_schedule():
    schedule.every().day.at("12:00").do(enviar_recordatorio_sync)
    print("⏰ Recordatorio programado para las 8:00 AM (12:00 UTC)")
    while True:
        schedule.run_pending()
        time.sleep(30)

# ── Inicio ──
if __name__ == "__main__":
    print("🤖 Bot iniciado con comandos /hoy y /listo")

    t = threading.Thread(target=hilo_schedule, daemon=True)
    t.start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("hoy", comando_hoy))
    app.add_handler(CommandHandler("listo", comando_listo))
    app.run_polling()