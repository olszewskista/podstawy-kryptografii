# Autor: Stanisław Olszewski

import sys

selected_mode = ""

for item in sys.argv[1:]:
    if not item.startswith("-"):
        continue
    for char in item:
        if char == "-":
            continue
        if char in ["p", "e", "k"]:
            if selected_mode == "":
                selected_mode = char
        else:
            print("Wrong option selected")
            sys.exit()


def read_text(name):
    try:
        with open(name, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("File", name, "not found")
        sys.exit()


def write_text(name, text):
    with open(name, "w") as file:
        file.write(text)


def prepare(text):
    line = ""
    final = ""
    text = text.lower()
    text = text.replace("\n", " ")
    for char in text:
        if ord(char) >= 97 and ord(char) <= 122 or ord(char) == 32:
            line += char
        if len(line) >= 64:
            final += line + "\n"
            line = ""
    remaining = 64 - len(line)
    if remaining > 0:
        final += line
        final += "x" * remaining
    return final


def encrypt(text, key):
    encrypted = []
    text = text.splitlines()
    key = "".join(format(ord(i), "08b") for i in key)

    for i in range(len(text)):
        new_line = ""
        line = " ".join(format(ord(i), "08b") for i in text[i])
        line = line.split(" ")

        for j in range(len(line)):
            while len(line[j]) != 8:
                line[j] = "0" + line[j]

        line = "".join(format(x) for x in line)

        if line != "00000000":
            for j in range(len(line)):
                xor = int(line[j]) ^ int(key[j])
                new_line = new_line + str(xor)
        encrypted.append(new_line)

    result = ""
    for row in encrypted:
        result += row + "\n"
    return result


def decrypt(crypto):
    crypto = crypto.strip().split("\n")
    for i in range(len(crypto)):
        line = crypto[i]
        temp = [line[j : j + 8] for j in range(0, len(line), 8)]
        crypto[i] = temp

    for i in range(len(crypto[0])):
        for j in range(len(crypto)):
            element = crypto[j][i]
            if len(element) > 1 and element[1] == "1":
                reset_key = element

                for k in range(len(crypto)):
                    encrypted_sign = crypto[k][i]
                    decrypted_sign = ""

                    for m in range(8):
                        xor = int(encrypted_sign[m]) ^ int(reset_key[m])
                        decrypted_sign += str(xor)

                    if decrypted_sign == "00000000":
                        crypto[k][i] = " "
                    else:
                        sign = chr(int(decrypted_sign, 2))
                        crypto[k][i] = sign

    result = ""
    for line in crypto:
        for sign in line:
            result += sign.lower()
        result += "\n"
    return result


def main():
    if selected_mode == "p":
        result = prepare(read_text("orig.txt"))
        write_text("plain.txt", result)
        print("Text prepared!")
    elif selected_mode == "e":
        result = encrypt(read_text("plain.txt"), read_text("key.txt"))
        write_text("crypto.txt", result)
        print("Text encrypted!")
    elif selected_mode == "k":
        result = decrypt(read_text("crypto.txt"))
        write_text("decrypt.txt", result)
        print("Text decrypted!")
    else:
        print("Wrong option selected")
        sys.exit()


if __name__ == "__main__":
    main()
