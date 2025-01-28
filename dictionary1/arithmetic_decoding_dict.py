# Read the encoded value from a file
def read_encoded_file(filename):
    with open(filename, 'r') as file:
        return float(file.read())

# Read probability ranges from a file
def read_probability_ranges(filename):
    ranges = {}
    with open(filename, 'r') as file:
        for line in file:
            char, range_ = line.strip().split(':', 1)
            low, high = map(float, range_.split(','))
            ranges[char] = (low, high)
    return ranges

# Arithmetic Decoding
def arithmetic_decoding(encoded_value, ranges):
    decoded_text = ''
    while True:
        for char, (low, high) in ranges.items():
            if low <= encoded_value < high:
                decoded_text += char
                encoded_value = (encoded_value - low) / (high - low)
                break
        else:
            break  # No matching range means decoding is done
    return decoded_text

# Main function for decoding
def main_decoding():
    encoded_value = read_encoded_file('arithmetic_encoded.txt')
    ranges = read_probability_ranges('arithmetic_dict.txt')
    
    decoded_text = arithmetic_decoding(encoded_value, ranges)
    
    with open('Arithmetic-Output.txt', 'w') as file:
        file.write(decoded_text)

if __name__ == '__main__':
    main_decoding()
