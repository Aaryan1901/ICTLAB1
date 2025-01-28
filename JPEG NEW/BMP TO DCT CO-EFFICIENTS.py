import numpy as np
from scipy.fftpack import dct
from PIL import Image

def apply_dct_to_block(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def process_image_with_dct(image):
    height, width = image.shape
    dct_coefficients = np.zeros_like(image, dtype=np.float32)

    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = image[i:i+8, j:j+8]
            dct_block = apply_dct_to_block(block)
            dct_coefficients[i:i+8, j:j+8] = dct_block

    return dct_coefficients

def main():
    image = Image.open('input.bmp').convert('L')
    image_array = np.array(image)

    dct_coefficients = process_image_with_dct(image_array)

    with open('dct.txt', 'w') as f:
        for row in dct_coefficients:
            f.write(' '.join(f'{val:.6f}' for val in row) + '\n')

    print("DCT coefficients have been saved to dct.txt.")

if __name__ == "__main__":
    main()
