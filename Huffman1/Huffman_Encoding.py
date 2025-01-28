import heapq
from collections import defaultdict


# Function to calculate frequency of characters in the input text
def calculate_frequency(text):
    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1
    return frequency


# Function to build the Huffman tree and return the character-to-code mapping
def build_huffman_tree(frequency):
    heap = [[weight, [char, ""]] for char, weight in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    huffman_dict = {pair[0]: pair[1] for pair in heap[0][1:]}
    return huffman_dict


# Function to encode the input text using the Huffman tree
def huffman_encoding(text):
    frequency = calculate_frequency(text)
    huffman_dict = build_huffman_tree(frequency)
    encoded_text = ''.join(huffman_dict[char] for char in text)
    return encoded_text, huffman_dict


# Function to write encoded text to a file
def write_encoded_file(encoded_text, filename):
    with open(filename, 'w') as file:
        file.write(encoded_text)


# Function to save the Huffman dictionary to a file
def write_huffman_dict(huffman_dict, filename):
    with open(filename, 'w') as file:
        for char, code in huffman_dict.items():
            file.write(f"{char}:{code}\n")


# Main function for encoding
def main_encoding():
    with open('Huff-input.txt', 'r') as file:
        text = file.read()

    encoded_text, huffman_dict = huffman_encoding(text)

    write_encoded_file(encoded_text, 'huffman.txt')
    write_huffman_dict(huffman_dict, 'huffman_dict.txt')


if __name__ == '__main__':
    main_encoding()
