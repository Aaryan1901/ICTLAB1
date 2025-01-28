# Function to read encoded message from a file
def read_encoded_file(filename):
    with open(filename, 'r') as file:
        return file.read()


# Function to read Huffman dictionary from a file
def read_huffman_dict(filename):
    huffman_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or ':' not in line:
                continue
            char, code = line.split(':', 1)
            huffman_dict[char] = code
    return huffman_dict


# Function to decode the Huffman encoded message
def huffman_decoding(encoded_text, huffman_dict):
    reverse_huffman_dict = {code: char for char, code in huffman_dict.items()}
    current_code = ''
    decoded_text = ''

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_huffman_dict:
            decoded_text += reverse_huffman_dict[current_code]
            current_code = ''

    return decoded_text


# Function to write decoded message to a file
def write_decoded_file(decoded_text, filename):
    with open(filename, 'w') as file:
        file.write(decoded_text)


# Main function for decoding
def main_decoding():
    encoded_text = read_encoded_file('huffman.txt')
    huffman_dict = read_huffman_dict('huffman_dict.txt')

    decoded_text = huffman_decoding(encoded_text, huffman_dict)
    write_decoded_file(decoded_text, 'Huff-Output.txt')


if __name__ == '__main__':
    main_decoding()
