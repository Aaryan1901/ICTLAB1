import wave
from collections import defaultdict


def read_wave_file(filename):
    """Read a WAV file and return the sample rate and signal."""
    with wave.open(filename, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        num_samples = wav_file.getnframes()
        signal = wav_file.readframes(num_samples)
        signal = [int.from_bytes(signal[i:i + 2], 'little', signed=True) for i in range(0, len(signal), 2)]
    return sample_rate, signal


def write_encoded_file(encoded_file, lpc_coeffs, signal):
    """Save LPC coefficients and original signal to a file."""
    with open(encoded_file, 'w') as f:
        f.write('LPC Coefficients: ' + ', '.join(map(str, lpc_coeffs)) + '\n')
        f.write('Original Signal: ' + ', '.join(map(str, signal)) + '\n')


def calculate_autocorrelation(signal, order):
    """Calculate the autocorrelation coefficients."""
    N = len(signal)
    r = [0] * (order + 1)
    for i in range(order + 1):
        r[i] = sum(signal[j] * signal[j - i] for j in range(i, N))
    return r


def linear_predictive_encode(signal, order=2):
    """Perform Linear Predictive Encoding."""
    r = calculate_autocorrelation(signal, order)

    # Create the autocorrelation matrix
    A = [[0] * order for _ in range(order)]
    for i in range(order):
        for j in range(order):
            A[i][j] = r[abs(i - j)]

    # Solve for LPC coefficients
    lpc_coeffs = [0] * order
    for i in range(order):
        if A[i][i] == 0:
            print("Diagonal element is zero. Encoding fallback triggered.")
            return [1.0] + [0.0] * (order - 1)
        for j in range(i + 1, order):
            ratio = A[j][i] / A[i][i]
            for k in range(order):
                A[j][k] -= ratio * A[i][k]
            r[j] -= ratio * r[i]

    # Back substitution
    for i in range(order - 1, -1, -1):
        lpc_coeffs[i] = r[i] / A[i][i]
        for j in range(i + 1, order):
            r[i] -= A[i][j] * lpc_coeffs[j]

    return lpc_coeffs


def main():
    input_filename = 'input_audio.wav'  # Replace with your input WAV file
    encoded_file = 'encoded_signal.lpc'
    order = 2  # LPC order

    # Read the input WAV file
    sample_rate, signal = read_wave_file(input_filename)

    print(f"Original signal (first 10 samples): {signal[:10]}")

    # Perform Linear Predictive Encoding
    lpc_coeffs = linear_predictive_encode(signal, order)
    print(f"LPC Coefficients: {lpc_coeffs}")

    # Save encoded data to file
    write_encoded_file(encoded_file, lpc_coeffs, signal)
    print(f"Encoded data saved to {encoded_file}.")


if __name__ == "__main__":
    main()
