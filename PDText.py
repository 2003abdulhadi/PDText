"""
PDText Script by Abdul Hadi 2023
Github Repo: https://github.com/2003abdulhadi/PDText
Usage is subject to license
"""

import os
import sys
import multiprocessing
from threading import Thread, Lock

import pytesseract
from pdf2image import convert_from_path as convert

cores: int = multiprocessing.cpu_count()
completed: int = 0
total: int = 0
lock: Lock = Lock()

"""
Tramslates the file at the filepath to text
The file is assumed to exist and be a pdf
"""
def translate(file: str) -> None:
    print("translating: " + file)

    pages = convert(file, 600);
    text = ""
    
    for page in pages:
        text += pytesseract.image_to_string(page)

    with open(f'{os.path.splitext(file)[0]}.txt', 'w') as f:
        f.write(text)

    global lock
    global completed
    global total

    lock.acquire()
    completed += 1
    print(f'done: {file}, {round((completed/total)*100, 2)}% completed')
    if(lock.locked()):
        lock.release()


def main():
    args = sys.argv[1:]

    files = [arg for arg in args if os.path.isfile(arg) and arg.lower().endswith('.pdf')]
    dirs = [arg for arg in args if os.path.isdir(arg)]

    if(not any([files, dirs])):
        print("No PDF files or directories provided")
        exit()

    threads: list[Thread] = []
    
    for filePath in files:
        threads.append(Thread(target=translate, args=[filePath]))

    for dir in dirs:
        for root, _, subfiles in os.walk(dir):
            for subfile in subfiles:
                if(subfile.lower().endswith('.pdf')):
                    filePath = root + "\\" + subfile
                    threads.append(Thread(target=translate, args=[filePath]))
                    
    global total
    total = len(threads)
    started: int = 0

    for thread in threads:
        thread.start()
        started += 1
        while(started - completed >= cores):
            pass

    for thread in threads:
        thread.join()
    

if __name__ == "__main__":
    main()
