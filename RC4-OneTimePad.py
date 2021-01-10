
#pre:none
#post: retval ascii values ==> string
def decipher(text):
    binary_values = text
    ascii_string = ""
    for binary_value in binary_values:
        ascii_character = chr(binary_value)
        ascii_string += ascii_character
    return ascii_string

#pre:none
#post: list of ascii values: plaintext_to_bits("abc") ====>[97,98,99]
def plaintext_to_bits(plaintext):
    temp=[ord(x) for x in plaintext]
    return temp

#pre:none
#post:ret ===>> [1,0,0,0,0]
def plainbits_to_encriptedbits(plaintext, key):
    plain_bits = plaintext_to_bits(plaintext)
    keyword_bits = plaintext_to_bits(key)
    encripted_bits = []
    for i in range(len(plain_bits)):
        encripted_bits.append(plain_bits[i] ^ keyword_bits[i])
    return encripted_bits

#pre:none
#post:
def one_time_pad(plaintext, key):
    encripted_bits = plainbits_to_encriptedbits(plaintext,key)
    text = encripted_bits
    encripted_message = decipher(text)
    return encripted_message

#pre:none
#post:#post:ret ===>> [1,0,0,1,0]
def plainbits_to_encriptedbits_rc4(plaintext, key):
    plain_bits = plaintext_to_bits(plaintext)
    keyword_bits = key
    encripted_bits = []
    for i in range(len(plain_bits)):
        encripted_bits.append(plain_bits[i] ^ keyword_bits[i])
    return encripted_bits

#pre:none
#post:
def encriptedbits_to_encriptedtext_rc4(plaintext, key):
    encripted_bits = plainbits_to_encriptedbits_rc4(plaintext, key)
    text = encripted_bits
    encripted_message = decipher(text)
    return encripted_message

#pre:none
#post:
def decrypt_text(enctext,key):
    enctext_bits=[ord(x) for x in enctext]
    keyword_bits = [ord(x) for x in key]
    dectext_bits =[]
    for i in range(len(enctext_bits)):
        dectext_bits.append(enctext_bits[i] ^ keyword_bits[i])
    decripted_message = decipher(dectext_bits)
    return decripted_message

#pre:none
#post:
def decrypt_text_rc4(enctext,key):
    enctext_bits=[ord(x) for x in enctext]
    keyword_bits = key
    dectext_bits =[]
    for i in range(len(enctext_bits)):
        dectext_bits.append(enctext_bits[i] ^ keyword_bits[i])
    decripted_message = decipher(dectext_bits)
    return decripted_message

#pre:none
#post: swaps two numbers in a list
def swap(list_to_swap,i,j):
    list_to_swap[i],list_to_swap[j]=list_to_swap[j],list_to_swap[i]
    return list_to_swap

#pre:none
#post:returns a random list of numbers from 1-256
def KSA(key):
    keylength = len(key)

    S = [x for x in range(256)]

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]  # swap

    return S

#pre:s must
#post:
def PRGA(S,len_text):
    i = 0
    j = 0
    K = []
    while len_text > 0:
        len_text = len_text-1
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # swap
        K.append( S[(S[i] + S[j]) % 256])
    return K

#pre: len_text.type()==int, type(key)== list[ord(char).....]
#post: returns a list of ascii values from a key using rc4 []
def RC4(key,len_text):
    S = KSA(key)
    return PRGA(S,len_text)

#pre:s must be a string
#post: returns a list of Ascii values  abc ==> [97,98,99]
def convert_key(s):
    return [ord(c) for c in s]


#pre:none
#post: menu ==1  ===> encripted msg using onetime pad
def menu():
    optionlist = {}
    optionlist['1']= "OneTime Pad."
    optionlist['2']= "RC4."
    optionlist['3']= "Exit"
    while optionlist != "3":
        print("\noptions: \n"
              "1:Onetime-Pad. \n"
              "2:Rc4\n"
              "3:Exit")
        selection=input("Please Select:")
        if selection =='1':
            plaintxt=str(input("Enter Text "))
            key=str(input("Enter key "))
            if len(key) == len(plaintxt):
                encriptedtxt=one_time_pad(plaintxt, key)
                print("Encripted Text :",repr(encriptedtxt),"\n")
                print("Decriptedtxt :",decrypt_text(encriptedtxt,key),"\n")
            else:
                print("size of key must equal to size of text \n")
        elif selection == '2':
            plaintxt = str(input("Enter Text "))
            key = convert_key(str(input("Enter key ")))
            keystream = RC4(key,len(plaintxt))
            encriptedtxt = encriptedbits_to_encriptedtext_rc4(plaintxt,keystream)
            print("Encripted Text :",repr(encriptedtxt),"\n")
            print("Decriptedtxt : " , decrypt_text_rc4(encriptedtxt,keystream),"\n")
        elif selection != '3':
            print("Unknown Option Selected!\n")
        else:
            print("exiting")
            break
menu()
