const botonIniciar =
    document.querySelector("#iniciar-control");

const reader =
    document.querySelector("#control-reader");

const resultado =
    document.querySelector("#resultado-control");

const errorControl =
    document.querySelector("#control-error");

const formBuscarControl =
    document.querySelector("#form-buscar-control");

const inputBuscarControl =
    document.querySelector("#buscar-control");

const resultadosBusquedaControl =
    document.querySelector(
        "#resultados-busqueda-control"
    );

const modalValidacion =
    document.querySelector("#modal-validacion");

const contenidoValidacion =
    document.querySelector("#contenido-validacion");


let scannerControl = null;
let scannerControlActivo = false;


async function detenerScanner() {
    if (scannerControl && scannerControlActivo) {
        try {
            await scannerControl.stop();
        } catch (error) {
            console.error(error);
        }
    }

    scannerControlActivo = false;
    reader.hidden = true;
}


async function mostrarEntrada(token) {
    const response = await fetch(
        `/api/entradas?q=${encodeURIComponent(token)}`
    );

    if (!response.ok) {
        throw new Error(
            "No se pudo consultar la entrada."
        );
    }

    const entradas = await response.json();

    const entrada = entradas.find(
        (item) => item.token === token
    );

    if (!entrada) {
        resultado.innerHTML = `
            <h2>Código no válido</h2>

            <p class="form-error">
                No existe una entrada asociada a este código.
            </p>
        `;

        resultado.hidden = false; 
        return;
    }

    let accion = "";

    if (entrada.estado === "ACTIVA") {
        accion = `
            <button
                id="autorizar-ingreso"
                class="button button-primary"
                type="button"
                data-token="${entrada.token}"
            >
                Autorizar ingreso
            </button>
        `;
    }

    contenidoValidacion.innerHTML = `
        <div class="validacion-estado">

            <h2>
                ${entrada.nombre}
            </h2>

            <div class="validacion-datos">

                <span>
                    Teléfono:
                    ${entrada.telefono || "—"}
                </span>

                <span>
                    Forma de pago:
                    ${entrada.forma_pago}
                </span>

                <span>
                    Estado:
                    ${entrada.estado}
                </span>

            </div>

            ${
                entrada.estado === "ACTIVA"
                    ? `
                        <div class="validacion-acciones">

                            <button
                                id="autorizar-ingreso"
                                class="button button-primary"
                                type="button"
                            >
                                Autorizar ingreso
                            </button>

                            <button
                                id="cerrar-validacion"
                                class="button"
                                type="button"
                            >
                                Cancelar
                            </button>

                        </div>
                    `
                    : `
                        <div class="validacion-acciones">

                            <button
                                id="cerrar-validacion"
                                class="button button-primary"
                                type="button"
                            >
                                Cerrar
                            </button>

                        </div>
                    `
            }

        </div>
    `;

    modalValidacion.hidden = false;

    document
    .querySelector("#cerrar-validacion")
    ?.addEventListener(
        "click",
        () => {
            modalValidacion.hidden = true;
        },
    );

    const botonAutorizar =
        document.querySelector("#autorizar-ingreso");

    botonAutorizar?.addEventListener(
        "click",
        async () => {
            botonAutorizar.disabled = true;
            botonAutorizar.textContent =
                "Validando...";

            try {
                const response = await fetch(
                    `/api/entradas/${token}/validar`,
                    {
                        method: "POST",
                    },
                );

                if (!response.ok) {
                    const error = await response.json();

                    throw new Error(
                        error.detail ||
                        "No se pudo validar la entrada."
                    );
                }

                const entradaValidada =
                    await response.json();

                contenidoValidacion.innerHTML = `
                    <div class="validacion-exitosa">

                        <div class="validacion-check">
                            ✓
                        </div>

                        <strong>
                            Validado con éxito
                        </strong>

                        <span>
                            ${entradaValidada.nombre}
                        </span>

                    </div>
                `;

                await new Promise(
                    (resolve) => setTimeout(resolve, 1400)
                );

                modalValidacion.hidden = true;

                contenidoValidacion.innerHTML = "";

                await iniciarScanner();

                resultado.hidden = false;

                await new Promise(
                    (resolve) => setTimeout(resolve, 1400)
                );

                resultado.hidden = true;

                await iniciarScanner();

                
            } catch (error) {
                resultado.innerHTML = `
                    <div class="control-result">

                        <h2>
                            Acceso rechazado
                        </h2>

                        <p class="form-error">
                            ${error.message}
                        </p>

                        <button
                            id="escanear-otra"
                            class="button button-primary"
                            type="button"
                        >
                            Escanear otra entrada
                        </button>

                    </div>
                `;

            }
        },
    );   
}


async function iniciarScanner() {
    resultado.hidden = true;
    errorControl.hidden = true;
    reader.hidden = false;

    scannerControl =
        new Html5Qrcode("control-reader");

    try {
        await scannerControl.start(
            {
                facingMode: "environment",
            },
            {
                fps: 10,

                qrbox: {
                    width: 200,
                    height: 200,
                },
            },

            async (decodedText) => {
                console.log(
                    "QR leído:",
                    decodedText
                );

                await detenerScanner();

                const token =
                    decodedText.trim();

                console.log(
                    "Token recibido:",
                    token
                );

                await mostrarEntrada(token);
            },

            () => {
                // Los intentos fallidos normales
                // de lectura se ignoran.
            },
        );

        scannerControlActivo = true;

    } catch (error) {
        console.error(
            "Error del scanner:",
            error
        );

        errorControl.textContent =
            "No se pudo acceder a la cámara.";

        errorControl.hidden = false;
    }
}

async function buscarEntradasControl(event) {
    event.preventDefault();

    const consulta =
        inputBuscarControl.value.trim();

    if (!consulta) {
        resultadosBusquedaControl.innerHTML = `
            <p class="form-error">
                Escribe un nombre, teléfono o código.
            </p>
        `;

        resultadosBusquedaControl.hidden = false;

        return;
    }

    resultadosBusquedaControl.innerHTML = `
        <p>Buscando...</p>
    `;

    resultadosBusquedaControl.hidden = false;

    try {
        const response = await fetch(
            `/api/entradas?q=${encodeURIComponent(consulta)}`
        );

        if (!response.ok) {
            throw new Error(
                "No se pudo realizar la búsqueda."
            );
        }

        const entradas = await response.json();

        if (entradas.length === 0) {
            resultadosBusquedaControl.innerHTML = `
                <p>
                    No se encontraron entradas.
                </p>
            `;

            return;
        }

        resultadosBusquedaControl.innerHTML =
            entradas
                .map(
                    (entrada) => `
                        <article class="result-item">

                            <div class="result-info">

                                <h3>
                                    ${entrada.nombre}
                                </h3>

                                <div class="result-meta">

                                    <span>
                                        Teléfono:
                                        ${entrada.telefono || "—"}
                                    </span>

                                    <span>
                                        Forma de pago:
                                        ${entrada.forma_pago}
                                    </span>

                                    <span>
                                        Estado:
                                        <span
                                            class="
                                                estado-badge
                                                estado-${entrada.estado.toLowerCase()}
                                            "
                                        >
                                            <span
                                                class="estado-dot"
                                            ></span>

                                            ${entrada.estado}
                                        </span>
                                    </span>

                                </div>

                            </div>

                            <div class="result-actions">

                                <button
                                    class="
                                        button
                                        button-primary
                                        seleccionar-entrada-control
                                    "
                                    type="button"
                                    data-token="${entrada.token}"
                                >
                                    Seleccionar
                                </button>

                            </div>

                        </article>
                    `
                )
                .join("");

    } catch (error) {
        console.error(error);

        resultadosBusquedaControl.innerHTML = `
            <p class="form-error">
                ${error.message}
            </p>
        `;
    }
}

botonIniciar?.addEventListener(
    "click",
    iniciarScanner,
);

formBuscarControl?.addEventListener(
    "submit",
    buscarEntradasControl,
);


resultadosBusquedaControl?.addEventListener(
    "click",
    async (event) => {
        const boton =
            event.target.closest(
                ".seleccionar-entrada-control"
            );

        if (!boton) {
            return;
        }

        const token =
            boton.dataset.token;

        await detenerScanner();

        resultadosBusquedaControl.hidden = true;

        await mostrarEntrada(token);
    },
);