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

def quantize_block(block, quant_matrix):
    return np.round(block / quant_matrix)

def process_dct_with_quantization(input_file, output_file, quant_matrix):
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

    with open(output_file, 'w') as f:
        for row in quantized_coefficients:
            f.write(' '.join(map(str, row)) + '\n')

    print(f"Quantized coefficients have been saved to {output_file}.")

if __name__ == "__main__":
    process_dct_with_quantization("dct.txt", "qntn.txt", QUANTIZATION_MATRIX)
