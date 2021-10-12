import os
import numpy as np
import mahotas
from glob import glob

from skimage import io, measure

HARALICK_FEATURES = [
    'angular_second_moment',
    'contrast',
    'correlation',
    'variance',
    'inverse_difference_moment',
    'sum_average',
    'sum_variance',
    'sum_entropy',
    'entropy',
    'difference_variance',
    'difference_entropy',
    'information_measure_1',
    'information_measure_2',
]

# expect images and masks within data directory
# expect masks to have "mask-" prepended to its corresponding image filename
img_paths = sorted(set(glob('data/*')) - set(glob('data/mask-*')))
mask_paths = sorted(glob('data/mask-*'))

img_path = img_paths[0]
mask_path = mask_paths[0]

img = io.imread(img_path)
mask = io.imread(mask_path)

img[~mask] = 0

# get region properties using scikit image, which gives the intensity image within ROI
props = measure.regionprops(mask, img)

# get haralick features using mahotas
features = mahotas.features.haralick(mask, distance=1)

# loop through the 2D array of 4 directions * 13 features
# get averages for each feature
feature_averages = {}

for index in range(len(HARALICK_FEATURES)):
    image_name = img_path
    feature_averages[HARALICK_FEATURES[index]] = np.mean([features[i][index] for i in range(4)])
    

print(feature_averages)

# tabulate and export to csv