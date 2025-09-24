import socket
import getpass

def main():
    """Main function for the client."""
    host = "127.0.0.1"
    port = 65432

    # Get the user's email details
    recipient_email = input("Enter the recipient's email address (your own): ")
    subject = input("Enter the email subject: ")
    
    # Collect multiline body more simply
    print("Enter the email body. Press Enter twice on an empty line to finish.")
    body_lines = []
    while True:
        line = input()
        if not line:
            break
        body_lines.append(line)
    body = "\n".join(body_lines).strip()

    # Create the message to send to the server
    message = f"{subject}<<<SEPARATOR>>>{body}<<<SEPARATOR>>>{recipient_email}"

    # Connect to the server and send the message
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        client_socket.sendall(message.encode("utf-8"))

        response = client_socket.recv(1024).decode("utf-8")
        print(f"Server response: {response}")

    except ConnectionRefusedError:
        print("Error: Could not connect to the server. Make sure the server.py script is running.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
