import os
import pandas as pd
import numpy as np
from glob import glob
from tqdm import tqdm
from skimage import io, img_as_ubyte

import texture


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


if __name__ == "__main__":
    print_banner()

    img_paths = sorted(set(glob("data/*")) - set(glob("data/*_mask.*")))
    mask_paths = sorted(glob("data/*_mask.*"))

    assert len(img_paths) == len(mask_paths), "Image and mask counts do not match."

    data = []

    print(f"\nAnalyzing a total of [ {len(img_paths) } ] images...\n")

    for index, path in tqdm(enumerate(img_paths), total=len(img_paths)):

        img = img_as_ubyte(io.imread(path))
        mask = io.imread(mask_paths[index])

        # assert np.ndim(img) == 2, "Image dimensions are incorrect. 2D image expected."
        # assert np.ndim(mask) == 2, "Mask dimensions are incorrect. 2D mask expected."
        assert np.ndim(img) == np.ndim(mask), "Image and mask dimensions do not match."

        # img_name = path.replace("images/", "")
        img_name = os.path.basename(path)

        features = texture.haralick(img, mask, distance=5)
        features["image_filename"] = img_name

        data.append(features)

    # convert to pandas dataframe and export to csv
    df = pd.DataFrame(data)
    columns = list(df)
    columns.insert(0, columns.pop(columns.index("image_filename")))

    df = df.loc[:, columns]

    if os.path.isdir("results") == False:
        os.mkdir("results")
    else:
        for path in glob("results/*"):
            os.remove(path)

    df.to_csv("results/results_5px.csv")

    # measure for 1px distance
    data = []

    print(f"\nAnalyzing a total of [ {len(img_paths) } ] images...\n")

    for index, path in tqdm(enumerate(img_paths), total=len(img_paths)):

        img = img_as_ubyte(io.imread(path))
        mask = io.imread(mask_paths[index])

        # assert np.ndim(img) == 2, "Image dimensions are incorrect. 2D image expected."
        # assert np.ndim(mask) == 2, "Mask dimensions are incorrect. 2D mask expected."
        assert np.ndim(img) == np.ndim(mask), "Image and mask dimensions do not match."

        # img_name = path.replace("images/", "")
        img_name = os.path.basename(path)

        features = texture.haralick(img, mask, distance=1)
        features["image_filename"] = img_name

        data.append(features)

    # convert to pandas dataframe and export to csv
    df = pd.DataFrame(data)
    columns = list(df)
    columns.insert(0, columns.pop(columns.index("image_filename")))

    df = df.loc[:, columns]

    df.to_csv("results/results_1px.csv")

    print(
        """

    Texture analysis complete. Results have been saved to the results directory.

    """
    )
