import socket
from des_tugas1 import encrypt, decrypt

def server_program():
    SHARED_KEY = "password"
    
    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many clients the server can listen simultaneously
    server_socket.listen(1)
    
    print(f"Server is running on {host}:{port} and waiting for clients...")
    print(f"Using shared key: {SHARED_KEY}")

    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    
    while True:
        # receive data stream. It won't accept data packet greater than 1024 bytes
        encrypted_data = conn.recv(1024).decode()
        if not encrypted_data:
            # if no data is received, break
            break
            
        # Decrypt message
        try:
            decrypted_data = decrypt(encrypted_data, SHARED_KEY)
            print("\nReceived message:", encrypted_data)
            print("\nDecrypted message:", decrypted_data)
        except Exception as e:
            print("Error decrypting message:", str(e))
            decrypted_data = "Error decrypting message"

        # Enter message
        data = input('\n -> ')
        if data.lower().strip() == 'bye':
            break
            
        # Encrypt message
        try:
            encrypted_data = encrypt(data, SHARED_KEY)
            conn.send(encrypted_data.encode())  # send data to the client
        except Exception as e:
            print("Error encrypting message:", str(e))
            conn.send("Error encrypting message".encode())

    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()