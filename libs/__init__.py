import builtins
from .utils import pd, np, px, ps, folium, haversine, clear_data, load_dataset, check_outliers, plot_histogram, plot_correlation
__all__ = ["pd", "np"]

for lib in __all__:
    setattr(builtins, lib, eval(lib))