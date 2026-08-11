# Entradas QR

Sistema web para la gestión de entradas QR para LITUAM perú.

## Tecnologías

- Python
- FastAPI
- SQLite
- Jinja2
- ReportLab
- Pillow

## Licencia

AGPL-3.0

## Despliegue en producción

La aplicación utiliza una configuración de Docker Compose separada para distinguir el entorno local del entorno de producción.

### Archivos de configuración

* `compose.yaml`: contiene la configuración base de la aplicación.
* `compose.prod.yaml`: añade la configuración específica del servidor de producción, como la conexión a la red externa `proxy` utilizada por Caddy.
* `.env`: contiene las variables de entorno y secretos. Este archivo no debe incluirse en el repositorio.
* `data/`: contiene la base de datos SQLite persistente y no forma parte de la imagen del contenedor.

La configuración de producción se obtiene combinando ambos archivos de Docker Compose.

### Comprobar la configuración

Antes de desplegar, se puede comprobar la configuración final resultante:

```bash
docker compose \
  -f compose.yaml \
  -f compose.prod.yaml \
  config
```

Esto permite verificar, entre otras cosas, que el volumen persistente de la base de datos y la red de producción estén configurados correctamente.

### Construir y levantar la aplicación

En producción:

```bash
docker compose \
  -f compose.yaml \
  -f compose.prod.yaml \
  up -d --build
```

Para comprobar el estado del servicio:

```bash
docker compose \
  -f compose.yaml \
  -f compose.prod.yaml \
  ps
```

### Actualizar una instalación existente

Después de publicar nuevos cambios en el repositorio, actualizar el servidor con:

```bash
git pull

docker compose \
  -f compose.yaml \
  -f compose.prod.yaml \
  up -d --build
```

La base de datos no se elimina durante este proceso.

El directorio:

```text
./data
```

se monta dentro del contenedor como:

```text
/app/data
```

De esta manera, los usuarios, entradas e historial permanecen almacenados fuera del ciclo de vida del contenedor y sobreviven a reconstrucciones o actualizaciones de la aplicación.

> **Importante:** no modificar directamente en producción archivos versionados del repositorio. Los cambios en el código o en la configuración de Docker deben realizarse en el repositorio local, publicarse en Git y posteriormente obtenerse en el servidor mediante `git pull`.

