# Webs cada 5 horas

Catálogo automático de sitios estáticos profesionales, responsive y sin gradientes. Cada edición usa HTML, CSS y JavaScript nativos, sin dependencias ni claves privadas.

## Cómo funciona

- GitHub Actions despierta cada hora y compara el instante actual con bloques UTC exactos de 5 horas.
- El generador crea una edición por cada bloque pendiente y recupera automáticamente bloques omitidos si GitHub retrasa una ejecución.
- La edición más reciente queda en `webs/`; el historial completo vive en `webs/sites/`.
- Cada cambio se valida y se publica como commit en `main`. GitHub puede retrasar los workflows programados, por lo que el commit puede aparecer después del límite lógico de cada bloque.

## Uso local

```bash
python scripts/generate_scheduled_site.py
python -B -m unittest discover -s tests -v
```

Para crear deliberadamente otra edición dentro del bloque actual:

```bash
python scripts/generate_scheduled_site.py --force
```

No se requiere instalación. Python 3.12 es suficiente.
