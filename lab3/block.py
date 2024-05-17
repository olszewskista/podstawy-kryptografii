# Autor: Stanisław Olszewski

from PIL import Image
from hashlib import md5


def get_key(block_size):
    keys = []
    for x in range(block_size):
        key = md5(str(288483 * x).encode()).digest()
        keys.append(key)

    return keys


def save_image(image_data, image_name, size):
    image_bytes = bytes(image_data)
    image = Image.frombytes("L", size, image_bytes)
    image.save(image_name)


def cbc(input_image, block_size, key):
    image_width, image_height = input_image.size
    image_data = input_image.tobytes()

    encrypted_image_data = []
    previous_element = 288483 % 256

    for y in range(image_height):
        for x in range(image_width):
            current_pixel = image_data[y * image_width + x]
            xored_with_previous = current_pixel ^ previous_element

            encrypted_pixel = xored_with_previous ^ key[x % block_size][y % block_size]

            previous_element = encrypted_pixel
            encrypted_image_data.append(encrypted_pixel)

    save_image(encrypted_image_data, "cbc_crypto.bmp", (image_width, image_height))


def ecb(input_image, block_size, key):
    image_width, image_height = input_image.size
    image_data = input_image.tobytes()

    encrypted_image_data = []

    for y in range(image_height):
        for x in range(image_width):
            current_pixel = image_data[y * image_width + x]
            encrypted_pixel = current_pixel ^ key[x % block_size][y % block_size]

            encrypted_image_data.append(encrypted_pixel)

    save_image(encrypted_image_data, "ecb_crypto.bmp", (image_width, image_height))


def main():
    input_image = Image.open("plain.bmp")

    BLOCK_SIZE = 8

    key = get_key(BLOCK_SIZE)

    ecb(input_image, BLOCK_SIZE, key)
    cbc(input_image, BLOCK_SIZE, key)


if __name__ == "__main__":
    main()
