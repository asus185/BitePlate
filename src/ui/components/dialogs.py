import customtkinter as ctk

class CustomDialog:
    """Maxsus dialog oynasi"""
    
    def __init__(self, title: str, message: str, parent=None):
        self._dialog = ctk.CTkToplevel(parent)
        self._dialog.title(title)
        self._dialog.geometry("400x200")
        self._dialog.grab_set()
        
        if parent:
            self._dialog.update_idletasks()
            x = parent.winfo_x() + (parent.winfo_width() - 400) // 2
            y = parent.winfo_y() + (parent.winfo_height() - 200) // 2
            self._dialog.geometry(f"400x200+{x}+{y}")
        
        label = ctk.CTkLabel(self._dialog, text=message, wraplength=350)
        label.pack(pady=20, padx=20)
        
        ok_btn = ctk.CTkButton(self._dialog, text="OK", command=self._dialog.destroy)
        ok_btn.pack(pady=10)
    
    def wait(self):
        self._dialog.wait_window()
