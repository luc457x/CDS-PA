import builtins
from .utils import pd, np
__all__ = ["pd", "np"]

for lib in __all__:
    setattr(builtins, lib, eval(lib))