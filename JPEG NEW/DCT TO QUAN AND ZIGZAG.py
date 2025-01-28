import numpy as np

QUANTIZATION_MATRIX = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
], dtype=np.float32)

# Function for quantization
def quantize_block(block, quant_matrix):
    return np.round(block / quant_matrix)

# Zigzag ordering function
def zigzag_order(block):
    zigzag_indices = [
        (0, 0), (0, 1), (1, 0), (2, 0), (1, 1), (0, 2), (0, 3), (1, 2),
        (2, 1), (3, 0), (4, 0), (3, 1), (2, 2), (1, 3), (0, 4), (0, 5),
        (1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (6, 0), (5, 1), (4, 2),
        (3, 3), (2, 4), (1, 5), (0, 6), (0, 7), (1, 6), (2, 5), (3, 4),
        (4, 3), (5, 2), (6, 1), (7, 0), (7, 1), (6, 2), (5, 3), (4, 4),
        (3, 5), (2, 6), (1, 7), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3),
        (7, 2), (7, 3), (6, 4), (5, 5), (4, 6), (3, 7), (4, 7), (5, 6),
        (6, 5), (7, 4), (7, 5), (6, 6), (5, 7), (6, 7), (7, 6), (7, 7)
    ]
    return [block[i, j] for i, j in zigzag_indices]

# Process DCT coefficients with quantization and Zigzag
def process_with_zigzag(input_file, quantized_file, zigzag_file, quant_matrix):
    with open(input_file, 'r') as f:
        dct_coefficients = np.array([
            list(map(float, line.strip().split()))
            for line in f.readlines()
        ])

    height, width = dct_coefficients.shape
    quantized_coefficients = np.zeros_like(dct_coefficients, dtype=np.int32)

    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = dct_coefficients[i:i+8, j:j+8]
            quantized_block = quantize_block(block, quant_matrix)
            quantized_coefficients[i:i+8, j:j+8] = quantized_block

    # Save quantized coefficients
    with open(quantized_file, 'w') as f:
        for row in quantized_coefficients:
            f.write(' '.join(map(str, row)) + '\n')

    # Zigzag transformation and saving to file
    with open(zigzag_file, 'w') as f:
        for i in range(0, height, 8):
            for j in range(0, width, 8):
                block = quantized_coefficients[i:i+8, j:j+8]
                zigzag_result = zigzag_order(block)
                f.write(' '.join(map(str, zigzag_result)) + '\n')

    print(f"Quantized coefficients saved to {quantized_file}.")
    print(f"Zigzag ordered coefficients saved to {zigzag_file}.")

if __name__ == "__main__":
    process_with_zigzag("dct.txt", "quantized.txt", "zigzag.txt", QUANTIZATION_MATRIX)
