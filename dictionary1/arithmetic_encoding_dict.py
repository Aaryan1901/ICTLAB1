from collections import defaultdict

# Calculate frequency of characters in the input text
def calculate_frequency(text):
    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1
    total_count = sum(frequency.values())
    probabilities = {char: freq / total_count for char, freq in frequency.items()}
    return probabilities, total_count

# Create probability ranges for each character
def create_probability_ranges(probabilities):
    low = 0.0
    ranges = {}
    for char, prob in sorted(probabilities.items(), key=lambda x: x[0]):
        high = low + prob
        ranges[char] = (low, high)
        low = high
    return ranges

# Arithmetic Encoding
def arithmetic_encoding(text, ranges):
    low, high = 0.0, 1.0
    for char in text:
        range_ = high - low
        high = low + range_ * ranges[char][1]
        low = low + range_ * ranges[char][0]
    return (low + high) / 2

# Main function for encoding
def main_encoding():
    with open('Arithmetic-input.txt', 'r') as file:
        text = file.read()
    
    probabilities, total_count = calculate_frequency(text)
    ranges = create_probability_ranges(probabilities)
    encoded_value = arithmetic_encoding(text, ranges)
    
    # Save encoded value and dictionary to files
    with open('arithmetic_encoded.txt', 'w') as file:
        file.write(str(encoded_value))
    
    with open('arithmetic_dict.txt', 'w') as file:
        for char, (low, high) in ranges.items():
            file.write(f"{char}:{low},{high}\n")

if __name__ == '__main__':
    main_encoding()
