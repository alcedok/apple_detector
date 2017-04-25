## Rudimentary Apple Detector Using Thresholding and Morphological Operations

```
Fall 2015
```

- Problem was simplified by making the assumption that apples to be detected were near/at the red color spectrum

### Approach

- Input image was converted into HSV color-space since hue stays constant in variable illumination environments, while RGB doesn’t.
- Input image is thresholded by red spectrum in HSV, changing pixels outside of red to black.
- Image is then converted to binary, keeping red colored pixels in white, and the rest black.
- Morphological operations are applied to the binary image, removing noise and separating individual blobs.
- Remaining blobs are filtered by their effective area on the image. Keeping those within the specified area.
- Detected apples are circled in the output image. 
