# 🗂️ Organizador de archivos con Python

Script de consola que **ordena automáticamente una carpeta desordenada** (por ejemplo, *Descargas*) moviendo cada archivo a una subcarpeta según su **tipo** o su **fecha de modificación**.

> Proyecto de práctica personal para demostrar automatización de tareas repetitivas con Python.

## ✨ Qué hace

- Agrupa por **tipo**: `Imagenes/`, `Documentos/`, `Hojas_de_calculo/`, `Audio/`, `Video/`, `Codigo/`, `Otros/`…
- Agrupa por **fecha**: `2026-08/`, `2026-09/`… (mes de última modificación).
- **Modo simulación** (`--simular`): muestra qué haría sin mover nada.
- **No sobrescribe**: si ya existe `tarea.pdf`, guarda el nuevo como `tarea (1).pdf`.
- Muestra un **resumen** al final con cuántos archivos movió por categoría.

```
Antes:                         Después (--modo tipo):
Descargas/                     Descargas/
├── foto.jpg                   ├── Imagenes/foto.jpg
├── tarea.pdf                  ├── Documentos/tarea.pdf
├── ventas.xlsx                ├── Hojas_de_calculo/ventas.xlsx
└── cancion.mp3                └── Audio/cancion.mp3
```

## 🛠️ Tecnologías

- Python 3.10+
- Solo biblioteca estándar: `pathlib`, `shutil`, `argparse`, `datetime`
- Pruebas con `unittest`

## ▶️ Cómo ejecutarlo

```bash
# 1. Clona el repositorio
git clone https://github.com/arumando/python-organizador-archivos.git
cd python-organizador-archivos

# 2. Primero simula (recomendado)
python organizador.py "C:/Users/TuUsuario/Downloads" --simular

# 3. Si el resultado te convence, ejecútalo de verdad
python organizador.py "C:/Users/TuUsuario/Downloads"

# Agrupar por mes en lugar de por tipo
python organizador.py "C:/Users/TuUsuario/Downloads" --modo fecha
```

Ejecutar las pruebas:

```bash
python -m unittest -v
```

## 📸 Capturas

[PENDIENTE: captura de la terminal ejecutando el script con `--simular`]

[PENDIENTE: captura de la carpeta antes y después]

## 📚 Qué aprendí

<!-- Revisa esta lista y escríbela con tus propias palabras. -->
- Manejar rutas de forma segura en Windows y Linux con `pathlib`.
- Crear una interfaz de línea de comandos con `argparse` (argumentos, opciones y ayuda).
- Diseñar un "modo simulación" antes de hacer cambios que no se pueden deshacer.
- Escribir pruebas automáticas con carpetas temporales (`tempfile`) para no tocar archivos reales.

## 🚀 Posibles mejoras

- Leer las categorías desde un archivo de configuración (JSON).
- Opción `--recursivo` para ordenar también las subcarpetas.
- Guardar un registro (log) para poder deshacer los movimientos.

## 👤 Autor

**José Armando García Bandera** — [github.com/arumando](https://github.com/arumando)
