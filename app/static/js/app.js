const generarForm = document.querySelector("#generar-form");

if (generarForm) {
    const resultado = document.querySelector("#resultado");
    const resultadoNombre = document.querySelector("#resultado-nombre");
    const resultadoImagen = document.querySelector("#resultado-imagen");
    const resultadoLink = document.querySelector("#resultado-link");
    const copiarLink = document.querySelector("#copiar-link");
    const formError = document.querySelector("#form-error");
    const nombreInput = document.querySelector("#nombre");

    generarForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        formError.hidden = true;
        resultado.hidden = true;

        const datos = {
            nombre: document.querySelector("#nombre").value.trim(),
            telefono: document.querySelector("#telefono").value.trim() || null,
            forma_pago: document.querySelector("#forma_pago").value,
        };

        try {
            const response = await fetch("/api/entradas", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify(datos),
            });

            if (!response.ok) {
                throw new Error("No se pudo generar la entrada.");
            }

            const entrada = await response.json();

            const urlPublica =
                `${window.location.origin}/e/${entrada.token}`;

            resultadoNombre.textContent = entrada.nombre;

            resultadoImagen.src =
                `/e/${entrada.token}/imagen`;

            resultadoLink.href = urlPublica;

            copiarLink.dataset.url = urlPublica;

            resultado.hidden = false;

            generarForm.reset();

            const irAlFinal = () => {
                window.scrollTo({
                    top: document.documentElement.scrollHeight,
                    behavior: "smooth",
                });
            };

            if (resultadoImagen.complete) {
                irAlFinal();
            } else {
                resultadoImagen.addEventListener(
                    "load",
                    irAlFinal,
                    { once: true }
                );
            }

        } catch (error) {
            formError.textContent = error.message;
            formError.hidden = false;
        }
    });

    copiarLink.addEventListener("click", async () => {
        const url = copiarLink.dataset.url;

        if (!url) {
            return;
        }

        await navigator.clipboard.writeText(url);

        const textoOriginal = copiarLink.textContent;

        copiarLink.textContent = "Enlace copiado";

        setTimeout(() => {
            copiarLink.textContent = textoOriginal;
        }, 1500);
    });
}