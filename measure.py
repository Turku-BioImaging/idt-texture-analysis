import os
import shutil
from typing import List
import pandas as pd
import numpy as np
from glob import glob
from tqdm import tqdm
from skimage import io, img_as_ubyte

import texture

IMG_DIR = "data/images"
MASK_DIR = "data/masks"
RESULTS_DIR = "results"


def print_banner():
    print(
        """
    ##################################################      
    --------------------------------------------------

    IMAGE TEXTURE ANALYSIS MODULE

    Turku BioImaging - Image Data Team
        Website: https://bioimaging.fi
        Repository: https://turku-bioimaging.github.io
        Email: image-data@bioimaging.fi
        
    --------------------------------------------------
    ##################################################
    """
    )


def _get_features(
    img: np.ndarray, mask: np.ndarray, distance: int = 5, mode: str = "max"
):
    channel_1 = img[:, 0, :, :]
    channel_2 = img[:, 1, :, :]

    # img_name = path.replace("images/", "")
    c1_fname = os.path.basename(path).replace(".tif", "_c1.tif")
    c2_fname = os.path.basename(path).replace(".tif", "_c2.tif")

    labels = _get_labels_from_mask(mask)
    data = []

    for idx, l in enumerate(labels):
        label = l.astype(np.uint8)

        features_c1 = texture.haralick(channel_1, label, distance, mode=mode)
        features_c1["image_filename"] = c1_fname
        features_c1["cell_id"] = idx + 1
        data.append(features_c1)

        features_c2 = texture.haralick(channel_2, label, distance, mode=mode)
        features_c2["image_filename"] = c2_fname
        features_c2["cell_id"] = idx + 1

        data.append(features_c2)

    return data


def _get_labels_from_mask(mask: np.ndarray) -> list:

    labels = []

    values = np.unique(mask).tolist()
    values.remove(0)
    for v in values:
        label = mask == v
        labels.append(label)

    return labels


def _save_data_to_file(data: List, fname: str):
    df = pd.DataFrame(data)

    columns = list(df)
    columns.insert(0, columns.pop(columns.index("image_filename")))
    columns.insert(1, columns.pop(columns.index("cell_id")))

    df = df.loc[:, columns]
    df.to_csv(f"results/{fname}.csv", index=False)


if __name__ == "__main__":
    print_banner()

    img_paths = sorted(glob(f"{IMG_DIR}/*"))
    mask_paths = sorted(glob(f"{MASK_DIR}/*"))

    assert len(img_paths) == len(mask_paths), "Image and mask counts do not match."

    print(f"\nAnalyzing {len(img_paths)} images using max intensity...\n")

    # measure texture with 5px distance and MIP
    data = []
    for index, path in tqdm(enumerate(img_paths), total=len(img_paths)):

        img = img_as_ubyte(io.imread(path))
        mask = io.imread(mask_paths[index])

        features = _get_features(img, mask, distance=5, mode="max")
        if len(features) > 0:
            [data.append(f) for f in features]

    _save_data_to_file(data, "texture_5px_max")

    # measure texture with 1px distance and MIP
    data = []
    for index, path in tqdm(enumerate(img_paths), total=len(img_paths)):

        img = img_as_ubyte(io.imread(path))
        mask = io.imread(mask_paths[index])

        features = _get_features(img, mask, distance=1, mode="max")
        if len(features) > 0:
            [data.append(f) for f in features]

    _save_data_to_file(data, "texture_1px_max")
