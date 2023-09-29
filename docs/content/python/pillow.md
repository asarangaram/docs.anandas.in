# `pillow`
`pillow` is the fork for PIL (Python Image Library) that has been discontinued from 2011. Pillow supports many image file formats.

## Working with HIEC

```bash
pip3 install pillow-heif
```
    
```python
from PIL import Image
from pillow_heif import register_heif_opener
    
register_heif_opener()
    
image = Image.open('image.heic')
```

## Crop a box from an Image

```python
    box = (x_offset, Y_offset, width, height)
    crop = image.crop(box)
    crop.save(image_path, format)
```

## Tutorials:

https://www.geeksforgeeks.org/python-pillow-tutorial/
https://www.udemy.com/course/python-pil-pillow-module-for-image-manipulation
