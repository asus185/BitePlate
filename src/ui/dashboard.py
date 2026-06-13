import customtkinter as ctk
from patterns.singleton import OrderHistoryLog

class ManagerDashboard(ctk.CTkFrame):
    """Manager dashboard"""
    
    def __init__(self, master, services):
        super().__init__(master)
        self._services = services
        self._order_log = OrderHistoryLog()
        self.pack(fill="both", expand=True)
        
        self._setup_ui()
    
    def _setup_ui(self):
        title = ctk.CTkLabel(self, text="Manager Dashboard", font=("Arial", 24, "bold"))
        title.pack(pady=(20, 10))
        
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        revenue = self._order_log.get_total_revenue()
        ctk.CTkLabel(stats_frame, text=f"Total Revenue: ${revenue:.2f}", font=("Arial", 16)).pack(pady=10)
        
        popular = self._order_log.get_most_frequent_item()
        if popular:
            ctk.CTkLabel(stats_frame, text=f"Most Popular: {popular}", font=("Arial", 14)).pack(pady=5)
        
        peak_hours = self._order_log.get_peak_hours()
        if peak_hours:
            peak_hour = max(peak_hours, key=peak_hours.get)
            ctk.CTkLabel(stats_frame, text=f"Peak Hour: {peak_hour}:00 ({peak_hours[peak_hour]} orders)", font=("Arial", 14)).pack(pady=5)
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(btn_frame, text="Refresh", command=self._refresh).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Export Report", command=self._export_report).pack(side="left", padx=5)
    
    def _refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._setup_ui()
    
    def _export_report(self):
        from ui.components.dialogs import CustomDialog
        CustomDialog("Report", "Report exported successfully!", self).wait()
