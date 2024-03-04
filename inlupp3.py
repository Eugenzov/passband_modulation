from cmath import sqrt
from numbers import Real
import matplotlib.pyplot as plt
import numpy as np

def channel2(transmittedSignal, noisePower):
    """
    Adds white and zero-mean circular symmetric complex Gaussian noise
    to all elements of transmittedSignal.

    Parameters:
    transmittedSignal : array_like
        Array containing transmitted signal symbols.
    noisePower : float
        Total noise power.

    Returns:
    noisySignal : array_like
        Array containing the received signal with added noise.
    """
    # Calculate the variance of the noise (divided by 2 for real and imaginary parts)
    noiseVar = noisePower / 2.0
    noisy_signal = []
    for i in range(len(transmittedSignal)):
        # Generate complex Gaussian noise with zero mean and specified variance
        noise_real = np.random.normal(loc=0 ,scale=np.sqrt(noiseVar))
        noise_imag = np.random.normal(loc=0 ,scale=np.sqrt(noiseVar))
        noise = noise_real + 1j * noise_imag
        noisy_signal.append(transmittedSignal[i] + noise)
    # Add noise to transmitted signal
    
    return noisy_signal

# Function to create QPSK symbols from binary message [01]
def create_QPSK_symbols(num_symbols,message):
    # Binary message [01]
    imaginary = [1j,-1j]
    real = [1,-1]
    
    qpsk_symbols = []
    for i in range(num_symbols):
        qpsk_symbols.append((imaginary[message[0]]+real[message[1]])/sqrt(2))
    # Repeat the message to create symbol vector
    
    # Map binary symbols to QPSK constellation points
    """
    qpsk_constellation = np.array([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j]) / np.sqrt(2)
    print(len(qpsk_constellation))
    qpsk_symbols = qpsk_constellation[symbol_vector]
    print(len(qpsk_symbols))
    """
    return qpsk_symbols

def calculate_SER(transmitted_symbols, received_symbols):
    num_errors = sum(transmitted_symbol != received_symbol for transmitted_symbol, received_symbol in zip(transmitted_symbols, received_symbols))
    SER = num_errors / len(transmitted_symbols)
    return SER

def decode_received_symbols(received_symbols):
    decoded_bits = []
    for symbol in received_symbols:
        decoded_bits.append(int(symbol.real > 0))
        decoded_bits.append(int(symbol.imag > 0))
    return decoded_bits





# Generate QPSK symbols
num_symbols = 1000
qpsk_symbols = create_QPSK_symbols(num_symbols,[0,1])
#print(qpsk_symbols)
# Different noise variances to test
noise_variances = [1, 0.1, 0.01]

# List to store received symbols for each noise variance
received_symbols_list = []

# Iterate over each noise variance and pass the symbols through the channel
for noise_variance in noise_variances:
    # Add noise to transmitted symbols
    
    noisy_symbols = channel2(qpsk_symbols, 2 * noise_variance)  # Multiply by 2 for complex noise variance
    
    # Append received symbols to the list
    received_symbols_list.append(noisy_symbols)
print(received_symbols_list)
# Plotting received symbols for different noise variances

SER_values = []
for i, received_symbols in enumerate(received_symbols_list):
    decoded_bits = decode_received_symbols(received_symbols)
    transmitted_bits = np.tile([0, 1], num_symbols // 2)
    SER = calculate_SER(transmitted_bits, decoded_bits)
    SER_values.append(SER)
    print(f"SER for Noise Variance {noise_variances[i]}: {SER}")
    
plt.figure(figsize=(10, 8))
for i in range(len(received_symbols_list)):
    real_part = []
    imag_part = []
    for j in received_symbols_list[i]:
        real_part.append(j.real)
        imag_part.append(j.imag)
    plt.scatter(real_part, imag_part, label=f"Noise Variance: {noise_variances[i]}")

plt.title("Received Symbols for Different Noise Variances")
plt.xlabel("Real Part")
plt.ylabel("Imaginary Part")
plt.legend()
plt.grid(True)

plt.show()

