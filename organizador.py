"""Organizador de archivos.

Ordena los archivos de una carpeta en subcarpetas según su tipo
(Imagenes, Documentos, Audio...) o según su fecha de modificación (2026-09).

Uso:
    python organizador.py RUTA_CARPETA [--modo tipo|fecha] [--simular]
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Categorías por extensión. Lo que no aparezca aquí va a "Otros".
CATEGORIAS = {
    "Imagenes": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "Documentos": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"},
    "Hojas_de_calculo": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentaciones": {".ppt", ".pptx", ".odp"},
    "Audio": {".mp3", ".wav", ".ogg", ".flac", ".m4a"},
    "Video": {".mp4", ".mkv", ".avi", ".mov", ".wmv"},
    "Comprimidos": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Codigo": {".py", ".c", ".java", ".html", ".css", ".js", ".sql", ".vhd"},
}


def categoria_por_tipo(archivo: Path) -> str:
    """Devuelve el nombre de la categoría según la extensión del archivo."""
    extension = archivo.suffix.lower()
    for categoria, extensiones in CATEGORIAS.items():
        if extension in extensiones:
            return categoria
    return "Otros"


def categoria_por_fecha(archivo: Path) -> str:
    """Devuelve 'AAAA-MM' según la fecha de modificación del archivo."""
    fecha = datetime.fromtimestamp(archivo.stat().st_mtime)
    return fecha.strftime("%Y-%m")


def destino_sin_conflicto(destino: Path) -> Path:
    """Si ya existe un archivo con ese nombre, agrega (1), (2)... al final."""
    if not destino.exists():
        return destino
    contador = 1
    while True:
        candidato = destino.with_name(f"{destino.stem} ({contador}){destino.suffix}")
        if not candidato.exists():
            return candidato
        contador += 1


def organizar(carpeta: Path, modo: str = "tipo", simular: bool = False) -> dict:
    """Mueve cada archivo de `carpeta` a la subcarpeta que le corresponde.

    Solo procesa archivos del primer nivel (no entra a subcarpetas) y
    omite archivos ocultos. Devuelve un resumen {categoria: cantidad}.
    """
    obtener_categoria = categoria_por_tipo if modo == "tipo" else categoria_por_fecha
    resumen = {}

    archivos = sorted(
        a for a in carpeta.iterdir() if a.is_file() and not a.name.startswith(".")
    )
    for archivo in archivos:
        categoria = obtener_categoria(archivo)
        destino = destino_sin_conflicto(carpeta / categoria / archivo.name)

        if simular:
            print(f"[SIMULACIÓN] {archivo.name} -> {categoria}/{destino.name}")
        else:
            destino.parent.mkdir(exist_ok=True)
            shutil.move(str(archivo), str(destino))
            print(f"{archivo.name} -> {categoria}/{destino.name}")

        resumen[categoria] = resumen.get(categoria, 0) + 1

    return resumen


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ordena los archivos de una carpeta en subcarpetas."
    )
    parser.add_argument("carpeta", type=Path, help="Carpeta que quieres ordenar")
    parser.add_argument(
        "--modo",
        choices=["tipo", "fecha"],
        default="tipo",
        help="Agrupar por tipo de archivo (por defecto) o por mes de modificación",
    )
    parser.add_argument(
        "--simular",
        action="store_true",
        help="Solo muestra lo que haría, sin mover nada",
    )
    args = parser.parse_args()

    if not args.carpeta.is_dir():
        print(f"Error: '{args.carpeta}' no es una carpeta válida.", file=sys.stderr)
        return 1

    resumen = organizar(args.carpeta, args.modo, args.simular)

    if not resumen:
        print("No hay archivos para organizar.")
        return 0

    print("\nResumen:")
    for categoria, cantidad in sorted(resumen.items()):
        print(f"  {categoria}: {cantidad} archivo(s)")
    print(f"  Total: {sum(resumen.values())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
