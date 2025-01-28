import heapq
from collections import defaultdict, Counter

# Huffman Node class
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Build Huffman Tree
def build_huffman_tree(frequencies):
    heap = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0]

# Generate Huffman Codes
def generate_huffman_codes(node, prefix="", codebook={}):
    if node:
        if node.char is not None:  # Leaf node
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

# Encode data using Huffman Codes
def huffman_encode(data, codebook):
    return "".join(codebook[char] for char in data)

# Decode Huffman-encoded data
def huffman_decode(encoded_data, root):
    decoded_data = []
    current_node = root
    for bit in encoded_data:
        current_node = current_node.left if bit == "0" else current_node.right
        if current_node.char is not None:  # Leaf node
            decoded_data.append(current_node.char)
            current_node = root
    return decoded_data

# Process Zigzag output with Huffman encoding
def process_huffman_encoding(input_file, encoded_file, huffman_codes_file):
    # Read the Zigzag-ordered coefficients
    with open(input_file, 'r') as f:
        zigzag_data = f.read().replace('\n', ' ')

    # Count frequencies of each symbol
    frequencies = Counter(zigzag_data.split())

    # Build Huffman Tree and Codes
    root = build_huffman_tree(frequencies)
    huffman_codes = generate_huffman_codes(root)

    # Encode Zigzag data
    encoded_data = huffman_encode(zigzag_data.split(), huffman_codes)

    # Save encoded data
    with open(encoded_file, 'w') as f:
        f.write(encoded_data)

    # Save Huffman codes
    with open(huffman_codes_file, 'w') as f:
        for char, code in huffman_codes.items():
            f.write(f"{char}:{code}\n")

    print(f"Huffman encoded data saved to {encoded_file}.")
    print(f"Huffman codes saved to {huffman_codes_file}.")

if __name__ == "__main__":
    process_huffman_encoding("zigzag.txt", "huffman_encoded.txt", "huffman_codes.txt")
