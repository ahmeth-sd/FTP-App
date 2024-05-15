import tkinter as tk
from tkinter import ttk, filedialog
import ftplib

class FTPClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FTP Client")

        #fullscreen
        self.root.state('zoomed')
        #self.root.geometry("1500x1080")

        self.ftp = None

        self.create_widgets()

    def create_widgets(self):
        # Connect Frame
        connect_frame = ttk.LabelFrame(self.root, text="Bağlantı")
        connect_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(connect_frame, text="IP Adresi:").grid(row=0, column=0, sticky="w")
        self.ent_ip = ttk.Entry(connect_frame)
        self.ent_ip.insert(0, "ftp.danzonn.com")
        self.ent_ip.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(connect_frame, text="Port:").grid(row=1, column=0, sticky="w")
        self.ent_port = ttk.Entry(connect_frame)
        self.ent_port.insert(0, "21")
        self.ent_port.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(connect_frame, text="Bağlan", command=self.connect_server).grid(row=2, column=0, columnspan=2, pady=5)

        # Server Messages
        self.text_servermsg = tk.Text(self.root, wrap=tk.WORD)
        self.text_servermsg.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Login Frame (Initially hidden)
        self.login_frame = ttk.LabelFrame(self.root, text="Giriş")

        ttk.Label(self.login_frame, text="Kullanıcı Adı:").grid(row=0, column=0, sticky="w")
        self.ent_login = ttk.Entry(self.login_frame)
        self.ent_login.insert(0, "ahmet@danzonn.com")
        self.ent_login.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.login_frame, text="Şifre:").grid(row=1, column=0, sticky="w")
        self.ent_pass = ttk.Entry(self.login_frame, show="*")
        self.ent_pass.insert(0, "MzjS7NK9dTUggPn4jVF9")
        self.ent_pass.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.login_frame, text="Giriş Yap", command=self.login_server).grid(row=2, column=0, columnspan=2, pady=5)

        # Directory Listing
        dir_frame = ttk.LabelFrame(self.root, text="Dizin Listesi")
        dir_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.libox_serverdir = tk.Listbox(dir_frame)
        self.libox_serverdir.pack(expand=True, fill="both")
        self.libox_serverdir.bind("<Double-Button-1>", self.listbox_double_click)

        # Commands Frame
        commands_frame = ttk.LabelFrame(self.root, text="Komutlar")
        commands_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")

        ttk.Label(commands_frame, text="Girdi:").grid(row=0, column=0, sticky="w")
        self.ent_input = ttk.Entry(commands_frame)
        self.ent_input.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        command_buttons = [
            ("Dizin Değiştir", self.change_directory),
            ("Dizin Oluştur", self.create_directory),
            ("Dizin Sil", self.delete_directory),
            ("Dosya Sil", self.delete_file),
            ("Dosya İndir", self.download_file),
            ("Dosya Yükle", self.upload_file),
            ("Bağlantıyı Kes", self.close_connection)
        ]

        for i, (text, command) in enumerate(command_buttons):
            ttk.Button(commands_frame, text=text, command=command, width=15).grid(row=i // 2 + 1, column=i % 2, padx=5, pady=5)

    def connect_server(self):
        ip = self.ent_ip.get()
        port = int(self.ent_port.get())
        try:
            self.ftp = ftplib.FTP()
            msg = self.ftp.connect(ip, port)
            self.text_servermsg.insert(tk.END, f"\n{msg}")
            self.login_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        except ftplib.all_errors as e:
            self.text_servermsg.insert(tk.END, f"\nHata: {e}")

    def login_server(self):
        user = self.ent_login.get()
        password = self.ent_pass.get()
        try:
            msg = self.ftp.login(user, password)
            self.text_servermsg.insert(tk.END, f"\n{msg}")
            self.display_dir()
            self.login_frame.grid_forget()
        except ftplib.all_errors as e:
            self.text_servermsg.insert(tk.END, f"\nHata: {e}")

    def display_dir(self):
        self.libox_serverdir.delete(0, tk.END)
        try:
            dirlist = self.ftp.nlst()
            for item in dirlist:
                self.libox_serverdir.insert(tk.END, item)
        except ftplib.all_errors as e:
            self.text_servermsg.insert(tk.END, f"\nHata: {e}")

    def change_directory(self):
        directory = self.ent_input.get()
        try:
            self.ftp.cwd(directory)
            self.display_dir()
        except ftplib.all_errors as e:
            self.text_servermsg.insert(tk.END, f"\nHata: {e}")

    def create_directory(self):
        directory = self.ent_input.get()
        try:
            self.ftp.mkd(directory)
            self.display_dir()
        except ftplib.all_errors as e:
            self.text_servermsg.insert(tk.END, f"\nHata: {e}")

    def delete_directory(self):
        directory = self.ent_input.get()
        try:
            self.ftp.rmd(directory)
            self.display_dir()
        except ftplib.all_errors as e:
            self.text_servermsg.insert(tk.END, f"\nHata: {e}")

    def delete_file(self):
        file = self.ent_input.get()
        try:
            self.ftp.delete(file)
            self.display_dir()
        except ftplib.all_errors as e:
            self.text_servermsg.insert(tk.END, f"\nHata: {e}")

    def download_file(self):
        file = self.ent_input.get()
        local_path = filedialog.asksaveasfilename(defaultextension="", initialfile=file)
        if not local_path:
            return  # Kullanıcı dosya seçimi yapmazsa işlemden çık

        try:
            with open(local_path, "wb") as f:
                self.ftp.retrbinary(f"RETR {file}", f.write)
            self.text_servermsg.insert(tk.END, f"\n{file} indirildi.")
        except ftplib.all_errors as e:
            self.text_servermsg.insert(tk.END, f"\nHata: {e}")

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return  # Kullanıcı dosya seçimi yapmazsa işlemden çık

        file_name = file_path.split("/")[-1]  # Dosya adını al
        try:
            with open(file_path, "rb") as f:
                self.ftp.storbinary(f"STOR {file_name}", f)
            self.text_servermsg.insert(tk.END, f"\n{file_name} yüklendi.")
            self.display_dir()  # Yüklemeden sonra dizini yenile
        except ftplib.all_errors as e:
            self.text_servermsg.insert(tk.END, f"\nHata: {e}")

    def listbox_double_click(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            item = widget.get(selection[0])
            self.ent_input.delete(0, tk.END)
            self.ent_input.insert(0, item)
            self.change_directory()

    def close_connection(self):
        if self.ftp:
            try:
                self.text_servermsg.insert(tk.END, "\nBağlantı kapatılıyor...")
                self.ftp.quit()
                self.ftp = None
                self.text_servermsg.insert(tk.END, "\nBağlantı kapatıldı.")
                self.libox_serverdir.delete(0, tk.END)  # Dizin listesini temizle
            except ftplib.all_errors as e:
                self.text_servermsg.insert(tk.END, f"\nHata: {e}")


# Uygulamayı başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = FTPClientApp(root)
    root.mainloop()

