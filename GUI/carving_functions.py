from PIL import Image
import os
import zipfile

stop_carving = False

# checks if a file is a valid zip file or not
def is_zip(file):
    try:
        with zipfile.ZipFile(file, "r") as zip_file:
            zip_file.testzip()
        return True
    except:
        return False

# checks which type of file a compressed file is
def check_zip_type(file):
    with zipfile.ZipFile(file, "r") as zip_file:
        names = zip_file.namelist()
    if '[Content_Types].xml' in names:
        if any(name.startswith('word/') for name in names):
            return "docx"
        elif any(name.startswith('ppt/') for name in names):
            return "pptx"
        elif any(name.startswith('xl/') for name in names):
            return "xlsx"
    else:
        return "zip"

def carve_jpeg(unallocated_dir, output):
    file_counter = 1
    jpeg_data = ''

    for root, _, files in os.walk(unallocated_dir):
        for file in files:
            file_path = os.path.join(unallocated_dir, root, file)
            fi = open(file_path, "rb")

            # loop to read each byte one at a time
            while True:
                if stop_carving:
                    fi.close()
                    break
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
                                    fo = open(output + "/jpeg_file_" + str(file_counter) + ".jpg", "wb")
                                    fo.write(jpeg_data)
                                    fo.close()

                                    try:
                                        img = Image.open(output + "/jpeg_file_" + str(file_counter) + ".jpg")
                                        img.verify()  # Verify the image to check for corruption.
                                        img.close()
                                        file_counter += 1
                                    except (IOError, SyntaxError) as e:
                                        os.remove(output + "/jpeg_file_" + str(file_counter) + ".jpg")

                                    jpeg_data = ''
                                    break
                                else:
                                    jpeg_data.extend(bytearray.fromhex(next_byte.hex()))
            fi.close()
    return 0

def carve_png(unallocated_dir, output):
    file_counter = 1
    png_data = ''

    for root, _, files in os.walk(unallocated_dir):
        for file in files:
            file_path = os.path.join(unallocated_dir, root, file)
            fi = open(file_path, "rb")
            # loop to read each byte one at a time
            while True:
                if stop_carving:
                    fi.close()
                    break
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
                                    fo = open(output + "/png_file_" + str(file_counter) + ".png", "wb")
                                    fo.write(png_data)
                                    fo.close()

                                    try:
                                        img = Image.open(output + "/png_file_" + str(file_counter) + ".png")
                                        img.verify()  # Verify the image to check for corruption.
                                        img.close()
                                        file_counter += 1
                                    except (IOError, SyntaxError) as e:
                                        try:
                                            img.close()
                                        except:
                                            print()
                                        os.remove(output + "/png_file_" + str(file_counter) + ".png")

                                    png_data = ''
                                    break
                                else:
                                    png_data.extend(bytearray.fromhex(next_byte.hex()))
            fi.close()

def carve_zip(unallocated_dir, output):
    zip_counter = 1
    docx_counter = 1
    pptx_counter = 1
    xlsx_counter = 1
    zip_data = ''

    for root, _, files in os.walk(unallocated_dir):
        for file in files:
            file_path = os.path.join(unallocated_dir, root, file)
            fi = open(file_path, "rb")
            # loop to read each byte one at a time
            while True:
                if stop_carving:
                    fi.close()
                    break
                byte = fi.read(1)
                if not byte:
                    break

                hex_byte = byte.hex()  # convert byte to hex
                # check if we are at a zip file header
                if hex_byte == "50":
                    next_bytes = fi.read(3)
                    header = hex_byte + next_bytes.hex()
                    # if we are at zip file header, start writing bytes to jpeg_data array
                    if header == "504b0304":
                        zip_data = bytearray.fromhex(header)
                        while True:
                            byte = fi.read(1)
                            if not byte:
                                break
                            hex_byte = byte.hex()

                            zip_data.extend(bytearray.fromhex(hex_byte))

                            # check if we are at the zip footer
                            if hex_byte == "50":
                                next_byte = fi.read(3)
                                footer = hex_byte + next_byte.hex()
                                if not next_byte:
                                    break
                                if footer == "504b0506":
                                    zip_data.extend(bytearray.fromhex(next_byte.hex()))
                                    next_byte = fi.read(18)
                                    zip_data.extend(bytearray.fromhex(next_byte.hex()))

                                    # open file to verify it is a valid zip file
                                    file_name = output + "/file"
                                    with open(file_name, "wb") as fo:
                                        fo.write(zip_data)

                                    # if it is a valid zip file, check which type it is
                                    if is_zip(file_name):
                                        zip_type = check_zip_type(file_name)
                                        if zip_type == "docx":
                                            os.rename(file_name, output + "/docx_file_" + str(docx_counter) + ".docx")
                                            docx_counter += 1
                                        elif zip_type == "pptx":
                                            os.rename(file_name, output + "/pptx_file_" + str(pptx_counter) + ".pptx")
                                            pptx_counter += 1
                                        elif zip_type == "xlsx":
                                            os.rename(file_name, output + "/xlsx_file_" + str(xlsx_counter) + ".xlsx")
                                            xlsx_counter += 1
                                        else:
                                            os.rename(file_name, output + "/zip_file_" + str(zip_counter) + ".zip")
                                            zip_counter += 1
                                    # if it is not a valid zip file, delete it
                                    else:
                                        os.remove(file_name)

                                    zip_data = ''
                                    break
                                else:
                                    zip_data.extend(bytearray.fromhex(next_byte.hex()))
            fi.close()
