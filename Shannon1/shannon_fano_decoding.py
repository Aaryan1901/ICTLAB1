# Read the encoded text from a file
def read_encoded_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Read Shannon-Fano codes from a file
def read_code_file(filename):
    codes = {}
    with open(filename, 'r') as file:
        for line in file:
            char, code = line.strip().split(':', 1)
            codes[code] = char
    return codes

# Decode the encoded text using Shannon-Fano codes
def shannon_fano_decoding(encoded_text, codes):
    current_code = ''
    decoded_text = ''
    for bit in encoded_text:
        current_code += bit
        if current_code in codes:
            decoded_text += codes[current_code]
            current_code = ''
    return decoded_text

# Write the decoded text to a file
def write_decoded_file(decoded_text, filename):
    with open(filename, 'w') as file:
        file.write(decoded_text)

# Main function for decoding
def main_decoding():
    encoded_text = read_encoded_file('shannon_fano_encoded.txt')
    codes = read_code_file('shannon_fano_dict.txt')
    decoded_text = shannon_fano_decoding(encoded_text, codes)
    write_decoded_file(decoded_text, 'Shannon-Output.txt')

if __name__ == '__main__':
    main_decoding()
