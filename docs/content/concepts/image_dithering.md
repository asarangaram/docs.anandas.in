

Image dithering is a technique used to reduce the number of colors in an image while maintaining the appearance of continuous-tone color gradations. When an image has more colors than can be displayed or printed, dithering helps approximate those colors by using a smaller palette. 

In a dithered image, the pixels are arranged in such a way that the human eye perceives the mixture of colors, creating the illusion of additional shades and smoother gradients. Dithering works by distributing the available colors across pixels based on the image's original colors and their intensities.

popular Algorithms

* **Floyd-Steinberg dithering**: distributes the error of color quantization to neighboring pixels to create a more visually pleasing result.
* **Ordered dithering**: uses a predefined dither matrix to distribute colors, creating the illusion of additional colors. The matrix is typically small, like 2x2 or 4x4.
* **Error diffusion dithering**:  distributes the color quantization error to neighboring pixels Similar to Floyd-Steinberg, but uses different diffusion matrices for better results.

