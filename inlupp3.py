from cmath import sqrt
from itertools import count
from numbers import Real
import matplotlib.pyplot as plt
import numpy as np

def channel2(transmittedSignal, noisePower):
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
def create_BPSK_symbols(message):
    # Binary message [01]
    imag = [-1j, 1j]
    qam_symbols = []
    for i in range(int(len(message))):
        index = message[i]
        qam_symbols.append(imag[index])
    return qam_symbols

def create_QPSK_symbols(num_symbols,message):
    # Binary message [01]
    imaginary = [1j,-1j]
    real = [1,-1]
    
    qpsk_symbols = []
    for i in range(num_symbols):
        qpsk_symbols.append((imaginary[message[0]]+real[message[1]])/sqrt(2))
    
    return qpsk_symbols

def create_16QAM_symbols(message):
    # Binary message [01]
    imaginary = [-1j, -1j/3, 1j, 1j/3]
    real = [1, 1/3, -1, -1/3]
    qam_symbols = []
    for i in range(int(len(message)/4)):
        index = message[i*4:i*4+4]
        real_index = int(''.join([str(bit) for bit in index[2:]]), 2)
        imag_index = int(''.join([str(bit) for bit in index[0:2]]), 2)
        qam_symbols.append((imaginary[imag_index] + real[real_index]) / sqrt(10))
    return qam_symbols

def decode_received_symbols(received_symbols,mode="QPSK"):
    decoded_bits = []
    if mode == "QPSK":
        for symbol in received_symbols:
            decoded_bits.append([int(symbol.imag < 0),int(symbol.real < 0)])
    elif mode == "BPSK":
        for symbol in received_symbols:
            decoded_bits.append([int(symbol.imag > 0)])
    elif mode == "16QAM":
        
        for symbol in received_symbols:
            cache = []

            if symbol.imag > 0:
                if symbol.imag > 2/(sqrt(10)*3).real:
                    cache.append(1)
                    cache.append(0)
                else:
                    cache.append(1)
                    cache.append(1)
            else:
                if symbol.imag < -2/(sqrt(10)*3).real:
                    cache.append(0)
                    cache.append(0)
                else:
                    cache.append(0)
                    cache.append(1)
            if symbol.real > 0:
                if symbol.real > 2/(sqrt(10)*3).real:
                    cache.append(0)
                    cache.append(0)
                else:
                    cache.append(0)
                    cache.append(1)
            else:
                if symbol.real < -2/(sqrt(10)*3).real:
                    cache.append(1)
                    cache.append(0)
                else:
                    cache.append(1)
                    cache.append(1)
            decoded_bits.append(cache)            
    return decoded_bits



def calculate_BER(transmitted_symbols, received_symbols):
    counter = 0
    transmitted_symbols = decode_received_symbols(transmitted_symbols)
    for i in range(len(transmitted_symbols)):
        for j in range(len(transmitted_symbols[i])):
            if transmitted_symbols[i][j]==received_symbols[i][j]:
                counter += 1
    return 1-counter/(len(transmitted_symbols)*len(transmitted_symbols[0]))

def calculate_SER(transmitted_symbols, received_symbols):
    counter = 0
    transmitted_symbols = decode_received_symbols(transmitted_symbols)
    for i in range(len(transmitted_symbols)):
        if transmitted_symbols[i]==received_symbols[i]:
            counter += 1
    return 1-counter/(len(transmitted_symbols))

# Generate QPSK symbols
num_symbols = 10000
qpsk_symbols = create_QPSK_symbols(num_symbols,[0,0])
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
#print(decode_received_symbols(received_symbols_list[1]))

# Plotting received symbols for different noise variances
print(decode_received_symbols(create_16QAM_symbols([0,1,0,1,1,1,0,0]),mode="16QAM"))
print(decode_received_symbols(create_BPSK_symbols([0,0,1,1,1]),mode="BPSK"))


"""
for i in range(len(received_symbols_list)):
    hej = decode_received_symbols(received_symbols_list[i]) 
    print("Symbol error rate is: "+str(calculate_SER(qpsk_symbols,hej)))
    print("Bit error rate is: "+str(calculate_BER(qpsk_symbols,hej)))
"""    

"""
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
"""