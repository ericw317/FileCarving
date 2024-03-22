from PIL import Image
import os
import tkinter
from tkinter import filedialog
from tkinter import messagebox

root = tkinter.Tk()
root.wm_attributes("-topmost", 1)
root.withdraw()

def carve_jpeg(file):
    file_counter = 1
    jpeg_data = ''
    fi = open(file, "rb")
    # loop to read each byte one at a time
    while True:
        byte = fi.read(1)
        if not byte:
            break

        hex_byte = byte.hex()  # convert byte to hex
        # check if we are at a jpeg file header
        if hex_byte == "ff":
            next_bytes = fi.read(3)
            header = hex_byte + next_bytes.hex()
            # if we are at jpeg file header, start writing bytes to jpeg_data array
            if header == "ffd8ffe0" or header == "ffd8ffe1":
                jpeg_data = bytearray.fromhex(header)
                while True:
                    byte = fi.read(1)
                    if not byte:
                        break
                    hex_byte = byte.hex()

                    jpeg_data.extend(bytearray.fromhex(hex_byte))

                    # check if we are at the jpeg footer
                    if hex_byte == "ff":
                        next_byte = fi.read(1)
                        if not next_byte:
                            break
                        if next_byte.hex() == "d9":
                            jpeg_data.extend(bytearray.fromhex(next_byte.hex()))
                            fo = open(output_directory + "/jpeg_file_" + str(file_counter) + ".jpg", "wb")
                            fo.write(jpeg_data)
                            fo.close()

                            try:
                                img = Image.open(output_directory + "/jpeg_file_" + str(file_counter) + ".jpg")
                                img.verify()  # Verify the image to check for corruption.
                                img.close()
                            except (IOError, SyntaxError) as e:
                                os.remove(output_directory + "/jpeg_file_" + str(file_counter) + ".jpg")

                            file_counter += 1
                            jpeg_data = ''
                            break
                        else:
                            jpeg_data.extend(bytearray.fromhex(next_byte.hex()))
    fi.close()

def carve_png(file):
    file_counter = 1
    png_data = ''
    fi = open(file, "rb")
    # loop to read each byte one at a time
    while True:
        byte = fi.read(1)
        if not byte:
            break

        hex_byte = byte.hex()  # convert byte to hex
        # check if we are at a png file header
        if hex_byte == "89":
            next_bytes = fi.read(7)
            header = hex_byte + next_bytes.hex()
            # if we are at png file header, start writing bytes to png_data array
            if header == "89504e470d0a1a0a":
                png_data = bytearray.fromhex(header)
                while True:
                    byte = fi.read(1)
                    if not byte:
                        break
                    hex_byte = byte.hex()

                    png_data.extend(bytearray.fromhex(hex_byte))

                    # check if we are at the png footer
                    if hex_byte == "00":
                        next_byte = fi.read(11)
                        footer = hex_byte + next_byte.hex()
                        if not next_byte:
                            break
                        if footer == "0000000049454e44ae426082":
                            png_data.extend(bytearray.fromhex(next_byte.hex()))
                            fo = open(output_directory + "/png_file_" + str(file_counter) + ".png", "wb")
                            fo.write(png_data)
                            fo.close()

                            try:
                                img = Image.open(output_directory + "/png_file_" + str(file_counter) + ".png")
                                img.verify()  # Verify the image to check for corruption.
                                img.close()
                            except (IOError, SyntaxError) as e:
                                os.remove(output_directory + "/png_file_" + str(file_counter) + ".png")

                            file_counter += 1
                            png_data = ''
                            break
                        else:
                            png_data.extend(bytearray.fromhex(next_byte.hex()))
    fi.close()


while True:
    selection = input("Which type of file would you like to carve?\n"
                      "1) JPEG\n"
                      "2) PNG\n"
                      "3) All of the above\n"
                      "0) Exit\n")
    while not selection.isnumeric() or int(selection) < 0 or int(selection) > 3:
        selection = input("Input must be a number between 0-2. Try again.\n")

    if int(selection) == 0:
        break

    messagebox.showinfo("File Selection", "Select the file you'd like to carve.")
    file_name = filedialog.askopenfilename()
    messagebox.showinfo("Output Selection", "Select the directory you'd like to output the files to.")
    output_directory = filedialog.askdirectory()

    if int(selection) == 1:
        carve_jpeg(file_name)
    elif int(selection) == 2:
        carve_png(file_name)
    elif int(selection) == 3:
        carve_jpeg(file_name)
        carve_png(file_name)
