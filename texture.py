import numpy as np
import mahotas
from skimage import measure

__HARALICK_FEATURES = [
    "angular_second_moment",
    "contrast",
    "correlation",
    "variance",
    "inverse_difference_moment",
    "sum_average",
    "sum_variance",
    "sum_entropy",
    "entropy",
    "difference_variance",
    "difference_entropy",
    "information_measure_1",
    "information_measure_2",
]


def haralick(image: np.ndarray, mask: np.ndarray, distance=5):
    """
    Takes a n-d image and mask and returns the 4-directional (2D images) or 13-directional (3D images) average of each of the 13 Haralick features.

    Parameters
    ----------
    image: ndarray
        n-dimensional ndarray
    mask: ndarray
        n-dimensional ndarray

    Returns
    -------
    feature_averages:
        A dictionary containing the directional averages of each Haralick feature.
    """

    image[~mask] = 0

    props = measure.regionprops(mask, image)

    # sanity check to make sure there is only one prop to deal with
    assert len(props) <= 1, "Number of region properties exceeds 1."

    # get haralick features using mahotas
    features = mahotas.features.haralick(
        props[0]["intensity_image"], distance=distance, ignore_zeros=True
    )

    # loop through the 2D array of 4 directions * 13 features
    # get averages for each feature
    feature_averages = {}

    for index in range(len(__HARALICK_FEATURES)):
        feature_averages[__HARALICK_FEATURES[index]] = np.mean(
            [features[i][index] for i in range(4)]
        )

    return feature_averages
