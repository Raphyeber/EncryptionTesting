import os
import threading
import queue

def decrypt(key, q):
    while True:
        file = q.get()
        if file is None:  # Signal to end the thread
            q.task_done()
            break
        try:
            key_index = 0
            max_key_index = len(key) - 1
            with open(file, 'rb') as f:
                data = f.read()
            decrypted_data = bytearray()
            for byte in data:
                decrypted_byte = byte ^ ord(key[key_index])
                decrypted_data.append(decrypted_byte)
                key_index = 0 if key_index >= max_key_index else key_index + 1
            with open(file, 'wb') as f:
                f.write(decrypted_data)
            print(f'{file} successfully decrypted')
        except Exception as e:
            print(f'Failed to decrypt {file}: {e}')
        q.task_done()

def start_decryption_process(key, abs_files):
    q = queue.Queue()
    threads = []
    for f in abs_files:
        q.put(f)
    for i in range(10):
        t = threading.Thread(target=decrypt, args=(key, q))
        t.daemon = True
        t.start()
        threads.append(t)
    for _ in range(10):
        q.put(None)
    q.join()
    for t in threads:
        t.join()
    print('Decryption complete')
    input("Press any key to exit...")

desktop_path = os.environ['USERPROFILE'] + '\\Desktop'
key_path = os.path.join(desktop_path, 'encryption_key.txt')
with open(key_path, 'r') as key_file:
    stored_key = key_file.read().strip()  # Read the stored key

files = os.listdir(desktop_path)
exclude_files = ['Enc.py', 'Dec.py', os.path.basename(__file__), 'encryption_key.txt']
abs_files = [os.path.join(desktop_path, f) for f in files if os.path.isfile(os.path.join(desktop_path, f)) and not f.endswith('.exe') and f not in exclude_files]

while True:
    key_input = input("Please enter the encryption key: ").strip()
    if not key_input:
        print("No key entered. Please enter a key.")
        continue
    if key_input != stored_key:
        print("Incorrect key. Please enter the correct key.")
        continue
    start_decryption_process(key_input, abs_files)
    break
