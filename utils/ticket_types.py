"""
TIPOS DE TICKET
Para añadir, quitar o editar una categoría, SOLO tienes que tocar esta lista.
El panel, los botones y el embed se generan solos a partir de ella.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class TicketType:
    key: str                        # Identificador interno (sin espacios, minúsculas)
    label: str                      # Texto del botón
    emoji: str
    description: str                # Texto que aparece en el panel
    category_id: int | None = None  # Categoría propia (si None, usa la de config)
    extra_role_ids: tuple = ()      # Roles extra que verán este tipo de ticket


TICKET_TYPES: list[TicketType] = [
    TicketType("soporte", "Soporte", "🛠️",
               "ayuda con problemas técnicos, configuración o funcionamiento del servidor."),
    TicketType("bugs", "Bugs", "🐛",
               "notificar errores o fallos detectados en el servidor."),
    TicketType("reportes", "Reportes", "🚨",
               "denunciar conductas o incumplimientos de normativa."),
    TicketType("apelaciones", "Apelaciones", "⚖️",
               "solicitar la revisión de una sanción apelable."),
    TicketType("donaciones", "Donaciones", "💎",
               "información sobre packs y compras."),
    TicketType("bandas", "Bandas", "🔫",
               "gestiones y consultas relacionadas con organizaciones criminales."),
    TicketType("ck", "CK", "☠️",
               "solicitar o gestionar un Character Kill."),
    TicketType("creadores", "Creadores", "🎥",
               "consultas sobre el programa de Creadores de Contenido."),
]


def get_type(key: str) -> TicketType | None:
    return next((t for t in TICKET_TYPES if t.key == key), None)
