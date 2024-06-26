import sys

if sys.version_info < (3, 8):  # pragma: no cover (<PY38)
    import importlib_metadata
else:  # pragma: no cover (PY38+)
    import importlib.metadata as importlib_metadata
try:
    VERSION = importlib_metadata.version('wyngman')
except Exception:
    VERSION = 'unknown'
