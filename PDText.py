"""
PDText Script by Abdul Hadi 2023
Github Repo: https://github.com/2003abdulhadi/PDText
Usage is subject to license
"""

import io
import os
import sys

import pytesseract
from PIL import Image
from wand.image import Image as Convert

"""
Tramslates the file at the filepath to text
The file is assumed to exist and be a pdf
"""
def translate(file: str) -> None:
    print("translating: " + file)
    with Convert(filename=file, resolution=300) as img:
        # set image properties
        img.format = 'tiff'
        img.compression_quality = 99

        # convert image to bytes, bytes to image, image to text
        value = img.make_blob()
        image = Image.open(io.BytesIO(value))
        text = pytesseract.image_to_string(image)

        # save text
        with open(f'{os.path.splitext(file)[0]}.txt', 'w') as f:
            f.write(text)

    print("done")

def main():
    args = sys.argv[1:]

    files = [arg for arg in args if os.path.isfile(arg) and arg.lower().endswith('.pdf')]
    dirs = [arg for arg in args if os.path.isdir(arg)]

    if(not any([files, dirs])):
        print("No files or directories provided")
        exit()

    for file in files:
        translate(file)

    for dir in dirs:
        for root, subdirs, subfiles in os.walk(dir):
            for subfile in subfiles:
                if(subfile.lower().endswith('.pdf')):
                    translate(root + "\\" + subfile)

if __name__ == "__main__":
    main()
