# Working with heic images on Python

Pillow / PIL can't open heic images by default. There are few options to open and working with heic images. Seems like, there are some license constrains to use ship with the hardware. Need to have a mechanism to download separately. (TODO: understand impact)
##     pillow-heif
This enables heic capability to pillow.
```bash
pip3 install pillow-heif
```
```python
from PIL import Image
from pillow_heif import register_heif_opener
    
register_heif_opener()
    
image = Image.open('image.heic')

#To save
image.save(filepath, format="jpg", ...)`
```
Found from [here](https://stackoverflow.com/a/69988418/8036094). This comes with [BSD-3-Clause license](https://github.com/bigcat88/pillow_heif/blob/master/LICENSE.txt). This is an Python bindings to  [`libheif`](https://github.com/strukturag/libheif) for working with HEIF images.

## pyheif
```base
pip install whatimage
pip install pyheif
```
```python
    import io
    
     import whatimage
     import pyheif
     from PIL import Image
    
    
     def decodeImage(bytesIo):
    
        fmt = whatimage.identify_image(bytesIo)
        if fmt in ['heic', 'avif']:
             i = pyheif.read_heif(bytesIo)
    
             # Extract metadata etc
             for metadata in i.metadata or []:
                 if metadata['type']=='Exif':
                     # do whatever
            
             # Convert to other file format like jpeg
             s = io.BytesIO()
             pi = Image.frombytes(
                    mode=i.mode, size=i.size, data=i.data)
    
             pi.save(s, format="jpeg")
```
Found from [here](https://stackoverflow.com/a/56946294/8036094). git [repo](https://github.com/carsales/pyheif)

Note, whatimage is a Python library to detect image type