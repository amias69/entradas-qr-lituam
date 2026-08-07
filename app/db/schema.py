SCHEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    activo INTEGER NOT NULL DEFAULT 1,
    creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS entradas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    telefono TEXT,
    forma_pago TEXT NOT NULL
        CHECK (forma_pago IN ('YAPE / PLIN', 'EFECTIVO')),
    generado_por INTEGER NOT NULL,
    estado TEXT NOT NULL DEFAULT 'ACTIVA'
        CHECK (estado IN ('ACTIVA', 'USADA', 'ANULADA')),
    creada_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usada_en TEXT,

    FOREIGN KEY (generado_por)
        REFERENCES usuarios(id)
);


CREATE TABLE IF NOT EXISTS historial_entradas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entrada_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    accion TEXT NOT NULL
        CHECK (
            accion IN (
                'CREADA',
                'EDITADA',
                'ANULADA',
                'VALIDADA'
            )
        ),
    fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (entrada_id)
        REFERENCES entradas(id),

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
);
"""