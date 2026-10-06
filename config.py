"""
CONFIGURACIÓN GENERAL
Aquí van los IDs y ajustes. Para cambiar algo del bot, empieza siempre por aquí.
(Activa el modo desarrollador en Discord -> clic derecho -> "Copiar ID")
"""
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# ---------- Servidor ----------
GUILD_ID = 0                     # ID del servidor de Barajas PD
TICKETS_CATEGORY_ID = 0          # Categoría donde se crean los tickets por defecto
LOGS_CHANNEL_ID = 0              # Canal donde se envían las transcripciones
STAFF_ROLE_IDS = [0]             # Roles que pueden ver/gestionar TODOS los tickets

# ---------- Apariencia ----------
EMBED_COLOR = 0x1E3A8A           # Azul oscuro
BANNER_URL = ""                  # URL de la imagen/banner del panel (opcional)
FOOTER_TEXT = "Barajas PD • Sistema de Tickets"

# ---------- Comportamiento ----------
MAX_OPEN_TICKETS_PER_USER = 1    # Tickets abiertos a la vez por usuario
AUTO_CLOSE_HOURS = 24            # Cierre automático por inactividad
AUTO_CLOSE_CHECK_MINUTES = 10    # Cada cuánto se revisa la inactividad

# ---------- Cogs (módulos) que se cargan al iniciar ----------
COGS = [
    "cogs.tickets",
]
