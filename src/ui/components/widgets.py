import customtkinter as ctk

class StatusBadge(ctk.CTkLabel):
    """Status badge komponenti"""
    
    def __init__(self, master, text: str, status: str):
        colors = {
            "Free": "#2ecc71",
            "Reserved": "#f39c12",
            "Occupied": "#e74c3c",
            "Awaiting Bill": "#3498db",
            "Cleared": "#95a5a6",
            "Pending": "#f39c12",
            "Confirmed": "#3498db",
            "Preparing": "#e67e22",
            "Ready": "#2ecc71",
            "Served": "#95a5a6",
            "Cancelled": "#e74c3c",
        }
        
        super().__init__(
            master,
            text=text,
            fg_color=colors.get(status, "#95a5a6"),
            text_color="white",
            corner_radius=5,
            padx=10,
            pady=5
        )
