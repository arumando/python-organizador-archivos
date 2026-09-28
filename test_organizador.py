"""Pruebas del organizador. Ejecutar con: python -m unittest"""

import tempfile
import unittest
from pathlib import Path

from organizador import categoria_por_tipo, organizar


class TestOrganizador(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.carpeta = Path(self._tmp.name)
        for nombre in ["foto.JPG", "tarea.pdf", "notas.txt", "cancion.mp3", "raro.xyz"]:
            (self.carpeta / nombre).write_text("contenido")

    def tearDown(self):
        self._tmp.cleanup()

    def test_categoria_ignora_mayusculas(self):
        self.assertEqual(categoria_por_tipo(Path("FOTO.PNG")), "Imagenes")

    def test_extension_desconocida_va_a_otros(self):
        self.assertEqual(categoria_por_tipo(Path("archivo.xyz")), "Otros")

    def test_organizar_por_tipo_mueve_archivos(self):
        resumen = organizar(self.carpeta, "tipo")
        self.assertEqual(resumen["Documentos"], 2)
        self.assertTrue((self.carpeta / "Imagenes" / "foto.JPG").exists())
        self.assertTrue((self.carpeta / "Otros" / "raro.xyz").exists())
        self.assertFalse((self.carpeta / "tarea.pdf").exists())

    def test_simular_no_mueve_nada(self):
        organizar(self.carpeta, "tipo", simular=True)
        self.assertTrue((self.carpeta / "tarea.pdf").exists())
        self.assertFalse((self.carpeta / "Documentos").exists())

    def test_no_sobrescribe_archivos_con_el_mismo_nombre(self):
        (self.carpeta / "Documentos").mkdir()
        (self.carpeta / "Documentos" / "tarea.pdf").write_text("original")
        organizar(self.carpeta, "tipo")
        self.assertEqual((self.carpeta / "Documentos" / "tarea.pdf").read_text(), "original")
        self.assertTrue((self.carpeta / "Documentos" / "tarea (1).pdf").exists())


if __name__ == "__main__":
    unittest.main()
