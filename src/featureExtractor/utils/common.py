import re
import os
import time
import urllib
import numpy as np
import pandas as pd
import requests
import multiprocessing
from pathlib import Path
from functools import partial
from PIL import Image
from tqdm import tqdm

from featureExtractor import constants

def common_mistake(unit):
    """
    Adjust units to match allowed formats.
    """
    if unit in constants.allowed_units:
        return unit
    if unit.replace('ter', 'tre') in constants.allowed_units:
        return unit.replace('ter', 'tre')
    if unit.replace('feet', 'foot') in constants.allowed_units:
        return unit.replace('feet', 'foot')
    return unit

def parse_string(s):
    """
    Parse a string into a number and unit.
    """
    s_stripped = "" if s is None or str(s) == 'nan' else s.strip()
    if s_stripped == "":
        return None, None
    pattern = re.compile(r'^-?\d+(\.\d+)?\s+[a-zA-Z\s]+$')
    if not pattern.match(s_stripped):
        raise ValueError(f"Invalid format in {s}")
    parts = s_stripped.split(maxsplit=1)
    number = float(parts[0])
    unit = common_mistake(parts[1])
    if unit not in constants.allowed_units:
        raise ValueError(f"Invalid unit [{unit}] found in {s}. Allowed units: {constants.allowed_units}")
    return number, unit

def create_placeholder_image(image_save_path):
    """
    Create a black placeholder image in case of a failed download.
    """
    try:
        placeholder_image = Image.new('RGB', (100, 100), color='black')
        placeholder_image.save(image_save_path)
    except Exception as e:
        print(f"Error creating placeholder image: {e}")

def download_image(image_link, save_folder, retries=3, delay=3):
    """
    Download an image from a link and save it to a specified folder.
    """
    if not isinstance(image_link, str):
        return

    filename = Path(image_link).name
    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):
        return

    for _ in range(retries):
        try:
            urllib.request.urlretrieve(image_link, image_save_path)
            return
        except Exception as e:
            print(f"Error downloading image {image_link}: {e}")
            time.sleep(delay)
    
    create_placeholder_image(image_save_path)

def download_images(image_links, download_folder, allow_multiprocessing=True):
    """
    Download multiple images from a list of links and save them to a specified folder.
    """
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    if allow_multiprocessing:
        download_image_partial = partial(
            download_image, save_folder=download_folder, retries=3, delay=3)

        # Limit the pool size to the number of available CPU cores
        pool_size = min(64, multiprocessing.cpu_count())
        with multiprocessing.Pool(processes=pool_size) as pool:
            list(tqdm(pool.imap(download_image_partial, image_links), total=len(image_links)))
    else:
        for image_link in tqdm(image_links, total=len(image_links)):
            download_image(image_link, save_folder=download_folder, retries=3, delay=3)



def normalize_units(value: float, unit: str) -> float:
    unit = unit.lower()
    if unit == 'milligram':
        return value / 1000
    elif unit == 'gram':
        return value
    elif unit == 'ounce':
        return value * 28.3495
    elif unit == 'fluid ounce':
        return value * 29.5735
    elif unit == 'centimetre':
        return value * 0.01
    elif unit == 'inch':
        return value * 0.0254
    else:
        raise ValueError(f"Unsupported unit: {unit}")
    


    # def processed_images(image_path , image_size):
    #     try:
    #         image = Image.open(image_path)


