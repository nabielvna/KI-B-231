import socket
from des_tugas1 import encrypt, decrypt

def client_program():
    SHARED_KEY = "password"
    
    host = '127.0.0.1'
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    
    print(f"Connected to server using shared key: {SHARED_KEY}")

    data = input('\n -> ')  # take input

    while data.lower().strip() != 'bye':
        # encrypt data
        try:
            encrypted_data = encrypt(data, SHARED_KEY)
            client_socket.send(encrypted_data.encode())  # send message
            print("Sent encrypted message:", encrypted_data) 
        except Exception as e:
            print("Error encrypting message:", str(e))
            client_socket.send("Error encrypting message".encode())

        encrypted_data = client_socket.recv(1024).decode()  # receive response
        # decrypt data
        try:
            decrypted_data = decrypt(encrypted_data, SHARED_KEY)
            print("\nReceived message:", encrypted_data)  # show in terminal
            print("\nDecrypted message:", decrypted_data)
        except Exception as e:
            print("Error decrypting message:", str(e))
            decrypted_data = "Error decrypting message"

        data = input('\n -> ')  # again take input

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()