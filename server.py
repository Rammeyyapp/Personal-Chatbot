
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- IMPORTANT SECURITY WARNING ---
# REPLACE these with your actual email and app password.
# NEVER share your password or commit this file with your password in it.
# You can generate an app password from your Google account security settings
# if you use Gmail.
SENDER_EMAIL = "aanadhia6@gmail.com"
SENDER_PASSWORD = "uxnh vwhw zeos pesj"

def send_email(subject, body, recipient):
    """Sends an email using the provided credentials."""
    try:
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = recipient
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server (for Gmail) and send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient, message.as_string())
        print(f"Email sent successfully to {recipient}!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def main():
    """Main function to run the server."""
    host = "127.0.0.1"
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server is listening on {host}:{port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Connection from {addr}")
            with conn:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break

                # The client sends the subject, body, and recipient separated by a special string
                try:
                    parts = data.split("<<<SEPARATOR>>>", 2)
                    if len(parts) == 3:
                        subject, body, recipient = parts
                        print(f"Received request to send email to {recipient} with subject '{subject}'.")
                        if send_email(subject, body, recipient):
                            conn.sendall(b"Success: Email sent.")
                        else:
                            conn.sendall(b"Error: Failed to send email.")
                    else:
                        conn.sendall(b"Error: Invalid data format.")
                except Exception as e:
                    print(f"Error processing data: {e}")
                    conn.sendall(b"Error: Internal server error.")

    except KeyboardInterrupt:
        print("\nServer is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
