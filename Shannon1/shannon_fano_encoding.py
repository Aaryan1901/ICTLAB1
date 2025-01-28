from collections import defaultdict


# Function to calculate the frequency of each character
def calculate_frequency(text):
    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1
    return dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))


# Recursive function to generate Shannon-Fano codes
def shannon_fano_coding(symbols, prefix=""):
    if len(symbols) == 1:
        return {symbols[0][0]: prefix}

    total_freq = sum(freq for _, freq in symbols)
    split_index, running_sum = 0, 0

    for i, (_, freq) in enumerate(symbols):
        running_sum += freq
        if running_sum >= total_freq / 2:
            split_index = i + 1
            break

    left = symbols[:split_index]
    right = symbols[split_index:]

    codes = {}
    codes.update(shannon_fano_coding(left, prefix + "0"))
    codes.update(shannon_fano_coding(right, prefix + "1"))
    return codes


# Function to encode the input text
def shannon_fano_encoding(text):
    frequency = calculate_frequency(text)
    codes = shannon_fano_coding(list(frequency.items()))
    encoded_text = ''.join(codes[char] for char in text)
    return encoded_text, codes


# Write the encoded text to a file
def write_encoded_file(encoded_text, filename):
    with open(filename, 'w') as file:
        file.write(encoded_text)


# Write the Shannon-Fano codes to a file
def write_code_file(codes, filename):
    with open(filename, 'w') as file:
        for char, code in codes.items():
            file.write(f"{char}:{code}\n")


# Main function for encoding
def main_encoding():
    with open('Shannon-input.txt', 'r') as file:
        text = file.read()

    encoded_text, codes = shannon_fano_encoding(text)
    write_encoded_file(encoded_text, 'shannon_fano_encoded.txt')
    write_code_file(codes, 'shannon_fano_dict.txt')


if __name__ == '__main__':
    main_encoding()
