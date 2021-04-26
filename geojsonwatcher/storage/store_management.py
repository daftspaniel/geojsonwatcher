import os
from pathlib import Path


def get_feature_store_path():
    config_folder = Path.joinpath(Path.joinpath(
        Path.home(), '.config'), 'geojsonwatcher')
    # Create config folder if it does not exist
    if not os.path.exists(config_folder):
        os.mkdir(config_folder)
    # Build path to our feature store database.
    return Path.joinpath(config_folder, 'quakes.db')
