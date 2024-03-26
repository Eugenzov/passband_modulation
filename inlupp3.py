from cmath import sqrt
from itertools import count
from numbers import Real
from statistics import variance
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import special
import math
from ham_encoding import flatten_list, binary_to_decimal, is_even, decimal_to_binary_bitstream, encodeHAM74, encodeHAM1511, decodeHAM74, decodeHAM1511

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
        qam_symbols.append((imaginary[imag_index] + real[real_index])*3 / sqrt(10))
    return qam_symbols

def decode_received_symbols(received_symbols,mode="QPSK"):
    decoded_bits = []
    if mode == "QPSK":
        for symbol in received_symbols:
            decoded_bits.append([int(symbol.imag < 0),int(symbol.real < 0)])
    elif mode == "BPSK":
        for symbol in received_symbols:
            #print(symbol)
            decoded_bits.append([int(symbol.imag > 0)])
    elif mode == "16QAM":
        
        for symbol in received_symbols:
            cache = []

            if symbol.imag > 0:
                if symbol.imag > 2/(sqrt(10)).real:
                    cache.append(1)
                    cache.append(0)
                else:
                    cache.append(1)
                    cache.append(1)
            else:
                if symbol.imag < -2/(sqrt(10)).real:
                    cache.append(0)
                    cache.append(0)
                else:
                    cache.append(0)
                    cache.append(1)
            if symbol.real > 0:
                if symbol.real > 2/(sqrt(10)).real:
                    cache.append(0)
                    cache.append(0)
                else:
                    cache.append(0)
                    cache.append(1)
            else:
                if symbol.real < -2/(sqrt(10)).real:
                    cache.append(1)
                    cache.append(0)
                else:
                    cache.append(1)
                    cache.append(1)
            decoded_bits.append(cache)            
    return decoded_bits

def calculate_BER(transmitted_symbols, received_symbols, modex = "QPSK"):
    counter = 0
    transmitted_symbols = decode_received_symbols(transmitted_symbols,mode=modex)
    received_symbols = decode_received_symbols(received_symbols,mode = modex)
    if modex == "BPSK":
        for i in range(len(transmitted_symbols)):
            if transmitted_symbols[i]==received_symbols[i]:
                counter += 1
    else:
        for i in range(len(transmitted_symbols)):
            for j in range(len(transmitted_symbols[i])):
                if transmitted_symbols[i][j]==received_symbols[i][j]:
                    counter += 1
    return 1-counter/(len(transmitted_symbols)*len(transmitted_symbols[0]))

def calculate_BER_ham74(transmitted_symbols, received_symbols, modex = "QPSK"):
    counter = 0
    transmitted_symbols = decode_received_symbols(transmitted_symbols,mode=modex)
    received_symbols = decodeHAM74(flatten_list(decode_received_symbols(received_symbols,mode = modex)) )

    if modex == "BPSK":
        for i in range(len(transmitted_symbols)):
            if transmitted_symbols[i][0]==received_symbols[i]:
                counter += 1
    else:
        for i in range(len(transmitted_symbols)):
            for j in range(len(transmitted_symbols[i])):
                if transmitted_symbols[i][j]==received_symbols[i][j]:
                    counter += 1
    return 1-counter/(len(transmitted_symbols)*len(transmitted_symbols[0]))

def calculate_BER_ham1511(transmitted_symbols, received_symbols, modex = "QPSK"):
    counter = 0
    transmitted_symbols = decode_received_symbols(transmitted_symbols,mode=modex)
    received_symbols = decodeHAM1511(flatten_list(decode_received_symbols(received_symbols,mode = modex)) )
    if modex == "BPSK":
        for i in range(len(received_symbols)):
            if transmitted_symbols[i][0]==received_symbols[i]:
                counter += 1
    else:
        for i in range(len(transmitted_symbols)):
            for j in range(len(transmitted_symbols[i])):
                if transmitted_symbols[i][j]==received_symbols[i][j]:
                    counter += 1
    return 1-counter/(len(transmitted_symbols)*len(transmitted_symbols[0]))

def calculate_SER(transmitted_symbols, received_symbols,modex = "QPSK"):
    counter = 0
    for i in range(len(transmitted_symbols)):
        if transmitted_symbols[i]==received_symbols[i]:
            counter += 1
        
    return 1-counter/(len(transmitted_symbols))

def calculate_snr(signal_power, noise_power):
    snr_db = 10 * math.log10(signal_power / noise_power)
    return snr_db

def Q(x):
    return 0.5 - 0.5 * special.erf(x/np.sqrt(2))
"""   
# Generate QPSK symbols
num_symbols = 10000
qpsk_symbols = create_QPSK_symbols(num_symbols,[0,0])

print(qpsk_symbols)
# Different noise variances to test
noise_variances = [1, 0.5, 0.1, 0.01]

# List to store received symbols for each noise variance
received_symbols_list = []

# Iterate over each noise variance and pass the symbols through the channel
for noise_variance in noise_variances:
    # Add noise to transmitted symbols
    
    noisy_symbols = channel2(qpsk_symbols, 2 * noise_variance)  # Multiply by 2 for complex noise variance
    
    # Append received symbols to the list
    received_symbols_list.append(noisy_symbols)
#print(decode_received_symbols(received_symbols_list[1]))
for i in range(len(received_symbols_list)):
    print("SER:"+ str(calculate_SER(received_symbols_list[i],qpsk_symbols))+" for variance power "+str(noise_variances[i]))
    print("BER:"+ str(calculate_BER(received_symbols_list[i],qpsk_symbols))+" for variance power "+str(noise_variances[i]))

"""
bin_rey = []
for i in range(int(1000*4)):
    bin_rey.append(random.randint(0,1))
ham74 = encodeHAM74(bin_rey)
ham1511 = encodeHAM1511(bin_rey)
var_rey = np.linspace(0.03,10,num=300)

emp_rey = []
theo_rey = []
ham_rey = []
for var in var_rey:
    #jenny_ham = create_BPSK_symbols(ham1511)
    jenny_ham = create_BPSK_symbols(ham74)
    jenny = create_BPSK_symbols(bin_rey)
    jenny2 = channel2(jenny,var)
    jenny_ham2 = channel2(jenny_ham,var)
    ham_rey.append(calculate_BER_ham74(jenny,jenny_ham2,modex="BPSK"))
    #ham_rey.append(calculate_BER_ham1511(jenny,jenny_ham2,modex="BPSK"))
    #theo_rey.append(Q(np.sqrt(12/(var*30))))
    theo_rey.append(Q(np.sqrt(2/var)))
    emp_rey.append(calculate_BER(jenny,jenny2,modex="BPSK"))

for i in range(len(var_rey)):    
    var_rey[i] = calculate_snr(1,var_rey[i])

plt.plot(var_rey,emp_rey,label='Empirical BER')
plt.plot(var_rey,theo_rey, label="Theoretical BER")
plt.plot(var_rey,ham_rey, label="Empirical Hamming code BER")
plt.title('BER vs SNR [dB]')
plt.xlabel('SNR [dB]')
plt.ylabel('BER')
plt.yscale('log')
plt.legend()
plt.show()
