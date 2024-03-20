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
                            file_counter += 1
                            jpeg_data = ''
                            break
                        else:
                            jpeg_data.extend(bytearray.fromhex(next_byte.hex()))
    fi.close()


messagebox.showinfo("File Selection", "Select the file you'd like to carve.")
file_name = filedialog.askopenfilename()
messagebox.showinfo("Output Selection", "Select the directory you'd like to output the files to.")
output_directory = filedialog.askdirectory()
carve_jpeg(file_name)