import os
import pandas as pd
import numpy as np
from glob import glob
from tqdm import tqdm
from skimage import io, measure

import texture

# Banner message
print(
    """
##################################################      
--------------------------------------------------

IMAGE TEXTURE ANALYSIS MODULE

Turku BioImaging - Image Data Team
    Website: https://bioimaging.fi
    Repository: https://turku-bioimaging.github.io
    Email: tbi-office@bioimaging.fi
    
--------------------------------------------------
##################################################
"""
)

img_paths = sorted(glob("images/*"))
mask_paths = sorted(glob("masks/*"))

assert len(img_paths) == len(mask_paths), "Image and mask counts do not match."

data = []

print(f"\nAnalyzing a total of [ {len(img_paths) } ] images...\n")

for index, path in tqdm(enumerate(img_paths), total=len(img_paths)):

    img = io.imread(path)
    mask = io.imread(mask_paths[index])

    assert np.ndim(img) == 2, "Image dimensions are incorrect. 2D image expected."
    assert np.ndim(mask) == 2, "Mask dimensions are incorrect. 2D mask expected."

    img_name = path.replace("images/", "")

    features = texture.haralick(img, mask)
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

df.to_csv("results/results.csv")

print(
    """
      
Texture analysis complete. Results have been saved to the results directory.

"""
)
