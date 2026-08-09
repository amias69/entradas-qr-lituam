const inputBusqueda = document.querySelector("#buscar-entrada");
const botonBuscar = document.querySelector("#buscar-button");
const resultados = document.querySelector("#resultados-busqueda");

const botonAbrirScanner = document.querySelector("#abrir-scanner");
const botonCerrarScanner = document.querySelector("#cerrar-scanner");

const scannerModal = document.querySelector("#scanner-modal");
const scannerError = document.querySelector("#scanner-error");

const modalAdministrar = document.querySelector("#modal-administrar");
const botonCerrarAdministrar = document.querySelector("#cerrar-modal-administrar");

let scanner = null;
let scannerActivo = false;


async function buscarEntrada() {
    const consulta = inputBusqueda.value.trim();

    resultados.innerHTML = "";

    if (!consulta) {
        return;
    }

    const response = await fetch(
        `/api/entradas?q=${encodeURIComponent(consulta)}`
    );

    if (!response.ok) {
        resultados.innerHTML = `
            <p class="form-error">
                No se pudo realizar la búsqueda.
            </p>
        `;

        return;
    }

    const entradas = await response.json();

    if (entradas.length === 0) {
        resultados.innerHTML = `
            <section class="card">
                No se encontraron entradas.
            </section>
        `;

        return;
    }

    entradas.forEach((entrada) => {
        const elemento = document.createElement("article");

        elemento.className = "result-item";

       const urlPublica =
            `${window.location.origin}/e/${entrada.token}`;

        const urlImagen =
            `/e/${entrada.token}/imagen`;

        elemento.innerHTML = `
        <div class="result-info">
            <h2>${entrada.nombre}</h2>

            <div class="result-meta">
                <span>
                    Teléfono:
                    ${entrada.telefono || "—"}
                </span>

                <span>
                    Forma de pago:
                    ${entrada.forma_pago}
                </span>

                <span class="estado">
                    Estado:
                    <span class="estado-badge estado-${entrada.estado.toLowerCase()}">
                        <span class="estado-dot"></span>
                        ${entrada.estado}
                    </span>
                </span>
            </div>
        </div>

        <div class="result-actions">

            <a
                class="button button-primary"
                href="${urlPublica}"
                target="_blank"
                rel="noopener"
            >
                Abrir entrada
            </a>

            <a
                class="button button-ghost"
                href="${urlImagen}"
                target="_blank"
                rel="noopener"
            >
                Ver imagen
            </a>

            <button
                class="button button-ghost copiar-link"
                type="button"
                data-url="${urlPublica}"
            >
                Copiar enlace
            </button>

            <button
                class="button button-primary administrar-entrada"
                type="button"
                data-id="${entrada.id}"
            >
                Administrar
            </button>

        </div>
    `;

        resultados.appendChild(elemento);

        const botonCopiar =
            elemento.querySelector(".copiar-link");

        botonCopiar.addEventListener(
            "click",
            async () => {
                const url = botonCopiar.dataset.url;

                await navigator.clipboard.writeText(url);

                const textoOriginal =
                    botonCopiar.textContent;

                botonCopiar.textContent =
                    "Enlace copiado";

                setTimeout(() => {
                    botonCopiar.textContent =
                        textoOriginal;
                }, 1500);
            },
        );

        const botonAdministrar =
            elemento.querySelector(".administrar-entrada");

        botonAdministrar.addEventListener(
            "click",
            () => {
                abrirModalAdministrar(
                    botonAdministrar.dataset.id
                );
            },
        );
    });
}

async function abrirModalAdministrar(entradaId) {
    modalAdministrar.dataset.entradaId = entradaId;
    modalAdministrar.hidden = false;

    const contenido =
        document.querySelector("#contenido-administrar");

    contenido.innerHTML = `
        <p class="page-description">
            Cargando entrada...
        </p>
    `;

    try {
        const response = await fetch(
            `/api/entradas/${entradaId}`
        );

        if (!response.ok) {
            throw new Error(
                "No se pudo cargar la entrada."
            );
        }

        const entrada = await response.json();

        const historialResponse = await fetch(
            `/api/entradas/${entradaId}/historial`
        );

        if (!historialResponse.ok) {
            throw new Error(
                "No se pudo cargar el historial."
            );
        }

        const historial = await historialResponse.json();

        const historialHtml = historial.length
        ? historial.map((registro) => `
            <div class="history-item">
                <strong>
                    ${registro.accion}
                </strong>

                <span>
                    ${registro.username}
                </span>

                <span>
                    ${registro.fecha}
                </span>
            </div>
        `).join("")
        : `
            <p class="page-description">
                Sin historial.
            </p>
        `;

        contenido.innerHTML = `
            <div class="entry-form">

                <div class="form-group">
                    <label for="administrar-nombre">
                        Nombre
                    </label>

                    <input
                        id="administrar-nombre"
                        type="text"
                        value="${entrada.nombre}"
                        ${entrada.estado === "ANULADA" ? "disabled" : ""}
                    >
                </div>

                <input
                    id="administrar-telefono"
                    type="tel"
                    inputmode="numeric"
                    pattern="[0-9]*"
                    value="${entrada.telefono || ""}"
                    oninput="this.value = this.value.replace(/[^0-9]/g, '')"
                    ${entrada.estado === "ANULADA" ? "disabled" : ""}
                >

                <div class="form-group">
                    <label for="administrar-forma-pago">
                        Forma de pago
                    </label>

                    <select id="administrar-forma-pago" ${entrada.estado === "ANULADA" ? "disabled" : ""}>

                        <option
                            value="YAPE / PLIN"
                            ${entrada.forma_pago === "YAPE / PLIN"
                                ? "selected"
                                : ""}
                        >
                            Yape / Plin
                        </option>

                        <option
                            value="EFECTIVO"
                            ${entrada.forma_pago === "EFECTIVO"
                                ? "selected"
                                : ""}
                        >
                            Efectivo
                        </option>

                        <option
                            value="CORTESÍA"
                            ${entrada.forma_pago === "CORTESÍA"
                                ? "selected"
                                : ""}
                        >
                            Cortesía
                        </option>

                    </select>
                </div>

                <div class="admin-meta">

                    <span>
                        Estado:
                        <strong>
                            ${entrada.estado}
                        </strong>
                    </span>

                    <span>
                        Generada por:
                        <strong>
                            ${entrada.generado_por_username || "—"}
                        </strong>
                    </span>

                    <span>
                        Fecha:
                        <strong>
                            ${entrada.creada_en}
                        </strong>
                    </span>

                </div>

                <div class="admin-section">
                    <h3>Historial</h3>

                    <div class="history-list">
                        ${historialHtml}
                    </div>
                </div>

                ${entrada.estado !== "ANULADA" ? `
                    <button
                        id="guardar-cambios"
                        class="button button-primary"
                        type="button"
                    >
                        Guardar cambios
                    </button>
                ` : ""}

                ${entrada.estado !== "ANULADA" ? `
                    <button
                        id="anular-entrada"
                        class="button button-danger"
                        type="button"
                    >
                        Anular entrada
                    </button>
                ` : ""}

            </div>
        `;

    } catch (error) {
        contenido.innerHTML = `
            <p class="form-error">
                ${error.message}
            </p>
        `;
    }
    const botonGuardar =
        document.querySelector("#guardar-cambios");

    botonGuardar?.addEventListener(
        "click",
        async () => {
            const datos = {
                nombre:
                    document
                        .querySelector("#administrar-nombre")
                        .value
                        .trim(),

                telefono:
                    document
                        .querySelector("#administrar-telefono")
                        .value
                        .trim() || null,

                forma_pago:
                    document
                        .querySelector("#administrar-forma-pago")
                        .value,
            };

            botonGuardar.disabled = true;
            botonGuardar.textContent = "Guardando...";

            try {
                const response = await fetch(
                    `/api/entradas/${entradaId}`,
                    {
                        method: "PUT",

                        headers: {
                            "Content-Type": "application/json",
                        },

                        body: JSON.stringify(datos),
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        "No se pudieron guardar los cambios."
                    );
                }

                botonGuardar.textContent = "Cambios guardados";

                await buscarEntrada();

                setTimeout(() => {
                    botonGuardar.textContent =
                        "Guardar cambios";

                    botonGuardar.disabled = false;
                }, 1500);

            } catch (error) {
                botonGuardar.textContent =
                    "Guardar cambios";

                botonGuardar.disabled = false;

                alert(error.message);
            }
        },
    );

    const botonAnular =
        document.querySelector("#anular-entrada");

    botonAnular?.addEventListener(
        "click",
        async () => {
            const confirmado = confirm(
                "¿Seguro que deseas anular esta entrada? Esta acción no se puede revertir."
            );

            if (!confirmado) {
                return;
            }

            const response = await fetch(
                `/api/entradas/${entradaId}/anular`,
                {
                    method: "POST",
                },
            );

            if (!response.ok) {
                alert(
                    "No se pudo anular la entrada."
                );

                return;
            }

            await buscarEntrada();

            cerrarModalAdministrar();
        },
    );
}


function cerrarModalAdministrar() {
    modalAdministrar.hidden = true;
    delete modalAdministrar.dataset.entradaId;
}

async function cerrarScanner() {
    if (scanner && scannerActivo) {
        try {
            await scanner.stop();
        } catch (error) {
            console.error(error);
        }
    }

    scannerActivo = false;
    scannerModal.hidden = true;
}


async function abrirScanner() {
    scannerError.hidden = true;
    scannerModal.hidden = false;

    scanner = new Html5Qrcode("qr-reader");

    try {
        await scanner.start(
            {
                facingMode: "environment",
            },
            {
                fps: 10,

                qrbox: {
                    width: 220,
                    height: 220,
                },
            },
            async (decodedText) => {

                await cerrarScanner();

                inputBusqueda.value = decodedText.trim();

                await buscarEntrada();
            },
            () => {
                // Los fallos normales de lectura se ignoran.
            },
        );

        scannerActivo = true;

    } catch (error) {
        scannerError.textContent =
            "No se pudo acceder a la cámara.";

        scannerError.hidden = false;
    }
}


botonBuscar?.addEventListener(
    "click",
    buscarEntrada,
);

inputBusqueda?.addEventListener(
    "keydown",
    (event) => {
        if (event.key === "Enter") {
            buscarEntrada();
        }
    },
);

botonAbrirScanner?.addEventListener(
    "click",
    abrirScanner,
);

botonCerrarScanner?.addEventListener(
    "click",
    cerrarScanner,
);

botonCerrarAdministrar?.addEventListener(
    "click",
    cerrarModalAdministrar,
);