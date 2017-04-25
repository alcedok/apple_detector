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


### Sample Results

---

<div style="text-align:center"><img width="739" alt="a" src="https://cloud.githubusercontent.com/assets/13475486/25365537/65ece204-2937-11e7-8c2d-e35c14a7c088.png"></div>.

---

<div style="text-align:center"><img width="586" alt="b" src="https://cloud.githubusercontent.com/assets/13475486/25365538/65f91998-2937-11e7-8f1c-27fba2e74fbc.png"></div>.

---

<div style="text-align:center"><img width="508" alt="c" src="https://cloud.githubusercontent.com/assets/13475486/25365539/65f9aac0-2937-11e7-8726-51558b2dbb0b.png"></div>.

---
