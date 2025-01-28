import wave
import struct

def read_encoded_file(encoded_file):
    """Read LPC coefficients and original signal from a file."""
    with open(encoded_file, 'r') as f:
        lines = f.readlines()
        lpc_coeffs = list(map(float, lines[0].split(':')[1].strip().split(',')))
        signal = list(map(int, lines[1].split(':')[1].strip().split(',')))
    return lpc_coeffs, signal

def write_wave_file(filename, sample_rate, signal):
    """Write a WAV file."""
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16 bits
        wav_file.setframerate(sample_rate)
        clamped_signal = [max(-32768, min(32767, int(sample))) for sample in signal]
        wav_file.writeframes(struct.pack(f'{len(clamped_signal)}h', *clamped_signal))

def linear_predictive_decode(lpc_coeffs, input_signal):
    """Decode the signal using LPC coefficients."""
    output_signal = [0] * len(input_signal)

    for n in range(len(input_signal)):
        output_signal[n] = input_signal[n]
        for k in range(1, len(lpc_coeffs)):
            if n - k >= 0:
                output_signal[n] -= lpc_coeffs[k] * output_signal[n - k]

    return output_signal

def main():
    encoded_file = 'encoded_signal.lpc'
    output_filename = 'decoded_audio.wav'
    sample_rate = 44100  # Replace with the correct sample rate

    # Read encoded data
    lpc_coeffs, input_signal = read_encoded_file(encoded_file)

    print(f"LPC Coefficients: {lpc_coeffs}")

    # Perform Linear Predictive Decoding
    decoded_signal = linear_predictive_decode(lpc_coeffs, input_signal)
    print(f"Decoded signal (first 10 samples): {decoded_signal[:10]}")

    # Write the decoded signal to a WAV file
    write_wave_file(output_filename, sample_rate, decoded_signal)
    print(f"Decoded audio saved to {output_filename}.")

if __name__ == "__main__":
    main()
