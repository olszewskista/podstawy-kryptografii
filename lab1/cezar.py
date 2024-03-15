#Autor: Stanisław Olszewski

import sys
import collections

selected_cipher = ''
selected_mode = ''

for arg in sys.argv[1:]:
    if not arg.startswith('-'): continue
    for char in arg:
        if char in ['c', 'a']:
            if selected_cipher == '': selected_cipher = char
            else: 
                print('You can only select one cipher')
                sys.exit()
        if char in ['e', 'd', 'j', 'k']:
            if selected_mode == '': selected_mode = char
            else: 
                print('You can only select one mode')
                sys.exit()

def read_text(name):
    try:
        with open(name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("File", name, "not found")
        sys.exit()
    
def write_text(name, text):
    with open(name, 'w') as file:
        file.write(text)

def nwd(a,b):
    while b != 0:
        a,b = b,a % b
    return a

def mod_inv(x):
    for b in range(26):
        if ((x * b) % 26) == 1:
            return b
        
def caesar(text, key):
    try:
        if key.startswith('--'):
            key = key[2:]
        key = int(key) % 26
    except:
        print('Key is not valid')
        sys.exit()
    result = ''
    for char in text:
        if not char.isalpha():
            result += char
            continue
        new_char = key + ord(char)
        if new_char > ord('z'):
            new_char -= 26
        elif new_char < ord('a'):
            new_char += 26
        
        result += chr(new_char)
    return result

def caesar_break_text(crypto, extra):
    if extra == '' or crypto == '':
        print('Crypto or extra text is empty')
        return None, None
    for extra_char, crypto_char in zip(extra, crypto):
        if not extra_char.isalpha(): continue
        for move in range(0, 26):
            char = ord(crypto_char) + move
            if char > 122:
                char -= 26
            if chr(char) == extra_char:
                found_key = 26 - move
                decrypted_text = caesar(crypto, '-' + str(found_key))
                return str(found_key), decrypted_text
    return None, None

def caesar_break_force(crypto):
    result = ''
    for move in range(1, 26):
        result += f'({move}) - '
        result += caesar(crypto, '-' + str(move))
        result += '\n'
    return result

def affine_encrypt(text, a, b):
    try:
        a = int(a)
        b = int(b)
        if nwd(a, 26) != 1: raise Exception
    except:
        print('Key is not valid')
        sys.exit()
    result = ''
    for char in text:
        if not char.isalpha():
            result += char
            continue
        new_char = ord(char) - 97
        new_char = (a * new_char + b) % 26
        new_char += 97
        result += chr(new_char)
    return result

def affine_decrypt(text, a, b):
    try:
        a = int(a)
        b = int(b)
        if nwd(a, 26) != 1: raise Exception
    except:
        print('Key is not valid')
        sys.exit()
    a_inv = mod_inv(a)
    if not a_inv:
        print('Could not find inverse of a')
        return
    result = ''
    for char in text:
        if not char.isalpha():
            result += char
            continue
        new_char = ord(char) - 97
        new_char = (a_inv * (new_char - b)) % 26
        new_char += 97
        result += chr(new_char)
    return result

def affine_break_text(crypto, extra):
    crypto_no_spaces = crypto.replace(' ', '')
    extra = extra.replace(' ', '')
    if extra == '' or crypto_no_spaces == '':
        print('Crypto or extra text is empty')
        return None, None
    possible_keys = []
    for extra_char, crypto_char in zip(extra, crypto_no_spaces):
        for a in range(1, 26):
            if nwd(a, 26) != 1: continue
            for b in range(26):
                encrypted_char = affine_encrypt(extra_char, a, b)
                if encrypted_char == crypto_char:
                    possible_keys.append((a, b))
                
    counter = collections.Counter(possible_keys)
    most_common_items = counter.most_common()
    most_common_count = most_common_items[0][1]
    if most_common_count > most_common_items[1][1]:
        key = most_common_items[0][0]
        decrypted_text = affine_decrypt(crypto, key[0], key[1])
        return key, decrypted_text 
    return None, None

def affine_break_force(crypto):
    result = ''
    for a in range(1, 26):
        if nwd(a, 26) != 1: continue
        for b in range(26):
            result += f'({a} {b}) - '
            result += affine_decrypt(crypto, a, b) + '\n'
    return result

def main():
    if selected_cipher == 'c' and selected_mode == 'e':
        print("You have selected caesar cipher encryption")
        result = caesar(read_text('plain.txt'), read_text('key.txt').split(' ')[0])
        if result:
            print('Encrypted text:', result)
            write_text('crypto.txt', result)
        else:
            print("No text provided")

    elif selected_cipher == 'c' and selected_mode == 'd':
        print("You have selected caesar cipher decryption")
        result = caesar(read_text('crypto.txt'), '-' + read_text('key.txt').split(' ')[0])
        if result:
            print('Decrypted text:', result)
            write_text('decrypt.txt', result)
        else:
            print("No text provided")

    elif selected_cipher == 'c' and selected_mode == 'j':
        print("You have selected caesar cipher cryptanalysis with text sample")
        found_key, result  = caesar_break_text(read_text('crypto.txt'), read_text('extra.txt'))
        if found_key and result:
            print("Found key:", found_key)
            print("Decrypted text:", result )
            write_text('key-found.txt', found_key)
            write_text('decrypt.txt', result)
        else:
            print("Key could not be found, try with different text sample")

    elif selected_cipher == 'c' and selected_mode == 'k':
        print('You have selected caesar cipher cryptogram cryptanalysis')
        result = caesar_break_force(read_text('crypto.txt'))
        if result:
            print("All combinations saved to decrypt.txt")
            write_text('decrypt.txt', result)

    elif selected_cipher == 'a' and selected_mode == 'e':
        print("You have selected affine cipher encryption")
        keys = read_text('key.txt').split(' ')
        result = affine_encrypt(read_text('plain.txt'), keys[0], keys[1])
        if result: 
            print("Encrypted text:", result)
            write_text('crypto.txt', result)
        else:
            print("No text provided")

    elif selected_cipher == 'a' and selected_mode == 'd':
        print("You have selected affine cipher decryption")
        keys = read_text('key.txt').split(' ')
        result = affine_decrypt(read_text('crypto.txt'), keys[0], keys[1])
        if result: 
            print('Decrypted text:', result)
            write_text('decrypt.txt', result)
        else:
            print("No text provided")

    elif selected_cipher == 'a' and selected_mode == 'j':
        print("You have selected affine cipher cryptanalysis with text sample")
        found_key, result = affine_break_text(read_text('crypto.txt'), read_text('extra.txt'))
        if result and found_key: 
            print("Found key:", found_key)
            print("Decrypted text:", result )
            write_text('key-found.txt', f"{found_key[0]} {found_key[1]}")
            write_text('decrypt.txt', result)
        else:
            print("Key could not be found, try with different text sample")

    elif selected_cipher == 'a' and selected_mode == 'k':
        print("You have selected affine cipher cryptogram cryptanalysis")
        result = affine_break_force(read_text('crypto.txt'))
        if result:
            print("All combinations saved to decrypt.txt")
            write_text('decrypt.txt', result)

    else:
        print("You have not selected correct cipher or mode")

if __name__ == '__main__':
    main()