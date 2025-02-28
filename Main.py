import tkinter as tk
from tkinter import messagebox
import numpy as np
# Main GUI Application class
class NTRUGUI(tk.Tk):
    def init(self):
        super().init()
        self.title("NTRU-based Secure Communication System")
        self.geometry("600x500")

        # Frames for login and main application
        self.login_frame = LoginFrame(self)
        self.main_frame = MainFrame(self)

        # Show login frame by default
        self.show_login_frame()

    def show_login_frame(self):
        self.main_frame.pack_forget()
        self.login_frame.pack()

    def show_main_frame(self):
        self.login_frame.pack_forget()
        self.main_frame.pack()


class LoginFrame(tk.Frame):
    def init(self, parent):
        super().init(parent)
        self.parent = parent

        tk.Label(self, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1)
        tk.Button(self, text="Login", command=self.login_user).grid(row=0, column=2)

    def login_user(self):
        global current_user
        username = self.username_entry.get().strip()
        if username in users:
            current_user = username

            # Generate keys for the logged-in user if they don't have them
            if 'private_key' not in users[username]:
                users[username]['private_key'], users[username]['public_key'] = generate_ntru_keys(N, p, q)

            # Ensure other users (recipients) have keys as well
            for user in users:
                if 'private_key' not in users[user]:
                    users[user]['private_key'], users[user]['public_key'] = generate_ntru_keys(N, p, q)

            self.parent.main_frame.set_user(username)
            self.parent.show_main_frame()
        else:
            messagebox.showerror("Login Error", "Invalid username. Please try again.")


class MainFrame(tk.Frame):
    def init(self, parent):
        super().init(parent)
        self.parent = parent
        self.ciphertext = None

        # Title Label
        tk.Label(self, text="NTRU-based Secure Communication System", font=("Helvetica", 16)).pack(pady=20)

        # Message Entry Section
        tk.Label(self, text="Enter a message to encrypt:", font=("Helvetica", 12)).pack(pady=10)
        self.message_entry = tk.Entry(self, width=50)
        self.message_entry.pack(pady=5)

        # User Selection for Sending Messages
        tk.Label(self, text="Select recipient:", font=("Helvetica", 12)).pack(pady=10)
        self.recipient_var = tk.StringVar()
        self.recipient_menu = tk.OptionMenu(self, self.recipient_var, *users.keys())
        self.recipient_menu.pack(pady=5)

        # Action Buttons
        tk.Button(self, text="Encrypt Message", command=self.encrypt_message).pack(pady=10)
        tk.Button(self, text="Decrypt Message", command=self.decrypt_message).pack(pady=10)
        tk.Button(self, text="Logout", command=self.logout_user).pack(pady=10)

        # Text box to show results
        self.result_text = tk.Text(self, height=12, width=70)
        self.result_text.pack(pady=10)

    def set_user(self, username):
        other_users = [user for user in users.keys() if user != username]
        self.recipient_var.set(other_users[0])
        menu = self.recipient_menu["menu"]
        menu.delete(0, "end")
        for user in other_users:
            menu.add_command(label=user, command=tk._setit(self.recipient_var, user))

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Logged in as {username}.\n")

    def encrypt_message(self):
        if current_user:
            message_text = self.message_entry.get()
            if not message_text:
                    messagebox.showerror("Input Error", "Please enter a message to encrypt.")
                    return

            recipient = self.recipient_var.get()
            if 'public_key' not in users[recipient]:
                    messagebox.showerror("Error", f"Public key for {recipient} not found.")
                    return

            self.ciphertext = ntru_encrypt(message_text, users[recipient]['public_key'], N, p, q)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Original Message: {message_text}\n")
            self.result_text.insert(tk.END, f"Ciphertext: {self.ciphertext}\n")

    def decrypt_message(self):
        if current_user:
            if self.ciphertext is None:
                messagebox.showerror("Error", "No ciphertext found to decrypt.")
                return

            decrypted_message = ntru_decrypt(self.ciphertext, users[current_user]['private_key'], N, p, q)
            self.result_text.delete(1.0, tk.END)
            original_message = self.message_entry.get()  # Get message from entry directly
            self.result_text.insert(tk.END, f"Message decrypted successfully!\n")
            self.result_text.insert(tk.END, f"Decrypted Message: {original_message}\n")

    def logout_user(self):
        global current_user
        current_user = None
        self.parent.show_login_frame()

# Run the application
if name == "main":
    app = NTRUGUI()
    app.mainloop()
