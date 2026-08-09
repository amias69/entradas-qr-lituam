# ==========================
# TOKEN DE ENTRADA
# ==========================

TOKEN_LENGTH = 20
TOKEN_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


# ==========================
# FORMAS DE PAGO
# ==========================

PAGO_YAPE_PLIN = "YAPE / PLIN"
PAGO_EFECTIVO = "EFECTIVO"

FORMAS_PAGO = (
    PAGO_YAPE_PLIN,
    PAGO_EFECTIVO,
)

PRECIO_ENTRADA = 60

# ==========================
# ESTADOS DE ENTRADA
# ==========================

ENTRADA_ACTIVA = "ACTIVA"
ENTRADA_USADA = "USADA"
ENTRADA_ANULADA = "ANULADA"


# ==========================
# ACCIONES DEL HISTORIAL
# ==========================

HISTORIAL_CREADA = "CREADA"
HISTORIAL_EDITADA = "EDITADA"
HISTORIAL_ANULADA = "ANULADA"
HISTORIAL_VALIDADA = "VALIDADA"