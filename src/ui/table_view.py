import customtkinter as ctk
from models.table import TableStatus

class TableView(ctk.CTkFrame):
    """Stollar ko'rinishi"""
    
    def __init__(self, master, table_service):
        super().__init__(master)
        self._table_service = table_service
        self.pack(fill="both", expand=True)
        
        self._setup_ui()
    
    def _setup_ui(self):
        title = ctk.CTkLabel(self, text="Table Management", font=("Arial", 24, "bold"))
        title.pack(pady=(20, 10))
        
        filter_frame = ctk.CTkFrame(self)
        filter_frame.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkLabel(filter_frame, text="Filter:").pack(side="left", padx=10)
        
        self._filter_var = ctk.StringVar(value="All")
        for status in ["All", "Free", "Reserved", "Occupied", "Awaiting Bill"]:
            ctk.CTkRadioButton(filter_frame, text=status, variable=self._filter_var, 
                              value=status, command=self._refresh_tables).pack(side="left", padx=5)
        
        self._table_frame = ctk.CTkScrollableFrame(self)
        self._table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self._refresh_tables()
    
    def _refresh_tables(self):
        for widget in self._table_frame.winfo_children():
            widget.destroy()
        
        filter_status = self._filter_var.get()
        if filter_status == "All":
            tables = self._table_service.get_all_tables()
        else:
            tables = self._table_service.get_tables_by_status(TableStatus(filter_status))
        
        colors = {
            "Free": "#2ecc71",
            "Reserved": "#f39c12",
            "Occupied": "#e74c3c",
            "Awaiting Bill": "#3498db",
            "Cleared": "#95a5a6"
        }
        
        for table in tables:
            card = ctk.CTkFrame(self._table_frame)
            card.pack(fill="x", pady=5, padx=10)
            
            info = ctk.CTkLabel(card, text=f"Table {table.table_number} ({table.capacity} seats)")
            info.pack(side="left", padx=10, pady=10)
            
            badge = ctk.CTkLabel(card, text=table.status.value, 
                                fg_color=colors.get(table.status.value, "#95a5a6"),
                                text_color="white", corner_radius=5, padx=10, pady=5)
            badge.pack(side="right", padx=10)
            
            loc = ctk.CTkLabel(card, text=table.location, text_color="gray")
            loc.pack(side="right", padx=5)
