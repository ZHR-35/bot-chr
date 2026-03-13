import schedule
import time
import asyncio
from datetime import datetime
from telegram import Bot
import os
TOKEN   = os.environ.get("TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))

bot = Bot(token=TOKEN)

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

async def enviar_mensaje(texto):
    async with Bot(token=TOKEN) as b:
        await b.send_message(chat_id=CHAT_ID, text=texto, parse_mode="Markdown")

def enviar_recordatorio():
    dia = datetime.now().strftime("%A")
    if dia not in horario:
        return

    mensaje = f"🗓 *{dias_es[dia]}* — Tu plan de hoy:\n\n"
    for tema, descripcion, tiempo in horario[dia]:
        mensaje += f"{tema}: {descripcion} — _{tiempo}_\n"
    mensaje += "\n💪 ¡Tú puedes! Un día a la vez."

    asyncio.run(enviar_mensaje(mensaje))
    print(f"✅ Recordatorio enviado — {dias_es[dia]}")

def enviar_prueba():
    mensaje = "✅ *Bot funcionando correctamente*\n\nVas a recibir tu horario todos los días a las 8:00 AM. 🎓"
    asyncio.run(enviar_mensaje(mensaje))
    print("✅ Mensaje de prueba enviado — revisa Telegram")

# ── Enviar prueba inmediata ──
print("🤖 Iniciando bot...")
enviar_prueba()

# ── Programar recordatorio diario a las 8:00 AM ──
schedule.every().day.at("08:00").do(enviar_recordatorio)
print("⏰ Recordatorio programado para las 8:00 AM todos los días")
print("Presiona Ctrl+C para detener\n")

while True:
    schedule.run_pending()
    time.sleep(30)