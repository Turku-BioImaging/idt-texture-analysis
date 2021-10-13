import os
import pandas as pd
from glob import glob

from skimage import io, measure

import texture

img_paths = sorted(set(glob('data/*')) - set(glob('data/mask-*')))
mask_paths = sorted(glob('data/mask-*'))


data = []

for index, path in enumerate(img_paths):

    img = io.imread(path)
    mask = io.imread(mask_paths[index])
    
    img_name = path.replace('data/', '')
    
    features = texture.haralick(img, mask)
    features['image_filename'] = img_name
    
    data.append(features)


# convert to pandas dataframe and export to csv
df = pd.DataFrame(data)
columns = list(df)
columns.insert(0, columns.pop(columns.index('image_filename')))

df = df.loc[:, columns]

if os.path.isdir('results') == False:
    os.mkdir('results')
else:
    for path in glob('results/*'):
        os.remove(path)

df.to_csv('results/results.csv')