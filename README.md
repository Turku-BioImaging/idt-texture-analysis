# Image Texture Analysis Module

This module accepts a 2D or 3D image and its corresponding mask and measures the 13 Haralick features. Each feature measurement is averaged across four directions (0°, 45°, 90°, and 135°) for 2D images, and 13 directions for 3D images, for rotational invariance.

The module is packaged into a Docker container image published at the [TBI-IDAT Container Repository](https://github.com/Turku-BioImaging/idt-texture-analysis/pkgs/container/idt-texture-analysis)

## How to use

#### Authentication

The container image is private at the moment, so it is not available to the public. You will need to login to the GitHub Container Repository in order to pull container images belonging to TBI-IDAT. Instructions on how to authenticate are [here](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) or you can contact [Junel Solis](mailto:junel.solis@abo.fi) for assistance.

### Expected Inputs

**Images** are expected to be 2- or 3-dimensional 8-bit images. They should be placed in a directory called **images** directly under the root directory of this project.

**Masks** are exptected to be 2- or 3-dimensional 8-bit images. They should be placed in a directory called **masks** directly under the root directory of this project.

**!!! IMPORTANT !!!**  
The images and their corresponding masks are sorted alphabetically by the module. Please make sure that the images and masks are in the same position within their folders. For example, if **image_3.tif** is the third file in **images**, then its **mask_3.tif** must be also the third file in **masks**. Otherwise, the output results will be INCORRECT.

When executed, this module will check that each image has equal dimensions to the corresponding mask and that the number of images in the **images** directory is equal to the number of masks in the **masks** directory. If these conditions are not met, the module will stop and print an error message.

### Run analysis

Run the following commands in the terminal:

```
cd <PROJECT-ROOT-FOLDER>
./run_docker.sh
```

The _run_docker.sh_ script simplifies pulling the container image and setting up volume mounts to the container. The script, when executed as-is, will output results provided there are images and masks present.

It is possible to use different directories for images and masks. In order to do this, the `docker run` command will need to be constructed manually with the appropriate bind mounts.

### Outputs

Analysis results are saved in the **results** directory within the project root.
