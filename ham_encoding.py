def flatten_list(lst):
    #flattens a recursive list
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened

def binary_to_decimal(binary_list):
    #returns a decimal value of a array bitstream
    decimal_value = 0
    power = len(binary_list) - 1
    for bit in binary_list:
        decimal_value += bit * (2 ** power)
        power -= 1
    return decimal_value

def is_even(bits):
    #takes a bitsream and returns true if even otherwise false
    counter = 0
    for i in ((bits)):
        if i == 1:
            counter += 1
    if counter%2 == 0:
        return True
    else:
        return False

def decimal_to_binary_bitstream(decimal_number):
    if decimal_number == 0:
        return [0]  # Special case for 0
    
    binary_bitstream = []
    while decimal_number > 0:
        binary_bitstream.append(decimal_number % 2)
        decimal_number //= 2
    
    # Reverse the list to get the correct bitstream order
    binary_bitstream.reverse()
    return binary_bitstream

def encodeHAM74(b): 
    #takes a number and encodes a message for PPMPMMM logic
    #remove incomplete messages
    if len(b)%4 !=0:
        b = b[:-int(len(b)%4)]
    c = []
    for i in range(int(len(b)/4)):
        tempbitstream = [1,1,b[i*4],1,b[1+i*4],b[2+i*4],b[3+i*4]]
        if is_even([b[i*4],b[1+i*4],b[3+i*4]]) == True:
            tempbitstream[0] = 0
        if is_even([b[i*4],b[2+i*4],b[3+i*4]]) == True:
            tempbitstream[1] = 0
        if is_even([b[1+i*4],b[2+i*4],b[3+i*4]]) == True:
            tempbitstream[3] = 0
        c.append(tempbitstream)
        c = flatten_list(c)
    return c 

def encodeHAM1511(b): 
    if len(b)%11 !=0:
        b = b[:-int(len(b)%11)]
    c = []
    for i in range(int(len(b)/11)):
        tempbitstream = [1,1,b[i*11],1,b[1+i*11],b[2+i*11],b[3+i*11],1,b[4+i*11],b[5+i*11],b[6+i*11],b[7+i*11],b[8+i*11],b[9+i*11],b[10+i*11]]
        if is_even([b[i*11],b[1+i*11],b[3+i*11],b[4+i*11],b[6+i*11],b[8+i*11],b[10+i*11]]) == True:
            tempbitstream[0] = 0
        if is_even([b[i*11],b[2+i*11],b[3+i*11],b[5+i*11],b[6+i*11],b[9+i*11],b[10+i*11]]) == True:
            tempbitstream[1] = 0
        if is_even([b[1+i*11],b[2+i*11],b[3+i*11],b[7+i*11],b[8+i*11],b[9+i*11],b[10+i*11]]) == True:
            tempbitstream[3] = 0
        if is_even(b[4:]) == True:
            tempbitstream[7]=0
        c.append(tempbitstream)
        c = flatten_list(c)
    return c 

def decodeHAM74(c): 
    decoded_bits = []
    for i in range(int(len(c)/7)):
        keybits = [0,0,0]
        if is_even([c[i*7],c[2+i*7],c[4+i*7],c[6+i*7]]) == False:
            keybits[2] = 1
        if is_even([c[1+i*7],c[2+i*7],c[5+i*7],c[6+i*7]]) == False:
            keybits[1] = 1
        if is_even([c[3+i*7],c[4+i*7],c[5+i*7],c[6+i*7]]) == False:
            keybits[0] = 1
        if keybits == [0,0,1]:
            if c[i*7] == 1:
                c[i*7] = 0
            else:
                c[i*7] = 1
        if keybits == [0,1,0]:
            if c[1+ i*7] == 1:
                c[1+i*7] = 0
            else:
                c[1+i*7] = 1
        if keybits == [0,1,1]:
            if c[2+i*7] == 1:
                c[2+i*7] = 0
            else:
                c[2+i*7] = 1
        if keybits == [1,0,0]:
            if c[3+i*7] == 1:
                c[3+i*7] = 0
            else:
                c[3+i*7] = 1
        if keybits == [1,0,1]:
            if c[4+i*7] == 1:
                c[4+i*7] = 0
            else:
                c[4+i*7] = 1
        if keybits == [1,1,0]:
            if c[5+i*7] == 1:
                c[5+i*7] = 0
            else:
                c[5+i*7] = 1
        if keybits == [1,1,1]:
            if c[6+i*7] == 1:
                c[6+i*7] = 0
            else:
                c[6+i*7] = 1
        decoded_bits.append([c[2+i*7],c[4+i*7],c[5+i*7],c[6+i*7]])
    return flatten_list(decoded_bits)
def decodeHAM1511(c): 
    decoded_bits = []
    for i in range(int(len(c)/15)):
        keybits = [0,0,0,0]
        if is_even([c[i*15],c[2+i*15],c[4+i*15],c[6+i*15],c[8+i*15],c[10+i*15],c[12+i*15],c[14+i*15]]) == False:
            keybits[3] = 1
        if is_even([c[1+i*15],c[2+i*15],c[5+i*15],c[6+i*15],c[9+i*15],c[10+i*15],c[13+i*15],c[14+i*15]]) == False:
            keybits[2] = 1
        if is_even([c[3+i*15],c[4+i*15],c[5+i*15],c[6+i*15],c[11+i*15],c[12+i*15],c[13+i*15],c[14+i*15]]) == False:
            keybits[1] = 1
        if is_even([c[7+i*15],c[8+i*15],c[9+i*15],c[10+i*15],c[11+i*15],c[12+i*15],c[13+i*15],c[14+i*15]]) == False:
            keybits[0] = 1
        if keybits != [0,0,0,0]:
            if c[binary_to_decimal(keybits)-1] == 1:
                c[binary_to_decimal(keybits)-1] = 0
            else:
                c[binary_to_decimal(keybits)-1] = 1
        (decoded_bits.append([c[2+i*15],c[4+i*15],c[5+i*15],c[6+i*15],c[8+i*15],c[9+i*15],c[10+i*15],c[11+i*15],c[12+i*15],c[13+i*15],c[14+i*15]]))
    return flatten_list(decoded_bits)
