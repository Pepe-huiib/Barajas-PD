# Barajas PD · Bot de Tickets

## Instalación
1. Python 3.10 o superior.
2. `pip install -r requirements.txt`
3. Copia `.env.example` a `.env` y pon el token del bot.
4. Rellena los IDs en `config.py`.
5. En el Developer Portal activa **Message Content Intent**.
6. `python main.py`
7. En el canal del panel, ejecuta `/panel`.

## Dónde cambiar cada cosa
| Quiero cambiar...                         | Archivo                  |
|-------------------------------------------|--------------------------|
| IDs, color, banner, límites, horas        | `config.py`              |
| Añadir/quitar/editar categorías y botones | `utils/ticket_types.py`  |
| Textos, normas y embeds                   | `utils/embeds.py`        |
| Cómo se crea/cierra un ticket             | `services/tickets.py`    |
| Botones dentro del ticket                 | `views/ticket_controls.py` |
| Comandos slash                            | `cogs/tickets.py`        |
| Añadir un módulo nuevo                    | crea `cogs/x.py` y añádelo a `COGS` en `config.py` |

## Comandos
`/panel` (admin) · `/cerrar [motivo]` · `/agregar @usuario` · `/quitar @usuario`

Permisos del bot: Gestionar canales, Ver canales, Enviar mensajes, Adjuntar archivos, Leer historial.
