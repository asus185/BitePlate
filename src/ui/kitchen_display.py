import customtkinter as ctk

class KitchenDisplay(ctk.CTkFrame):
    """Oshxona displeyi"""
    
    def __init__(self, master, kitchen_service, table_service=None):
        super().__init__(master)
        self._kitchen_service = kitchen_service
        self._table_service = table_service
        self.pack(fill="both", expand=True)
        
        self._setup_ui()
    
    def _setup_ui(self):
        title = ctk.CTkLabel(self, text="Kitchen Queue", font=("Arial", 24, "bold"))
        title.pack(pady=(20, 10))
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(btn_frame, text="Process Next", command=self._process_next).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Process All", command=self._process_all).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Undo Last", command=self._undo_last, fg_color="orange").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Refresh", command=self._refresh_queue).pack(side="left", padx=5)
        
        self._queue_frame = ctk.CTkScrollableFrame(self)
        self._queue_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self._history_frame = ctk.CTkFrame(self)
        self._history_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self._history_frame, text="Completed Orders", font=("Arial", 14, "bold")).pack(pady=5)
        self._history_list = ctk.CTkScrollableFrame(self._history_frame, height=100)
        self._history_list.pack(fill="x", padx=10, pady=5)
        
        self._refresh_queue()
    
    def _refresh_queue(self):
        for widget in self._queue_frame.winfo_children():
            widget.destroy()
        
        queue = self._kitchen_service.queue.queue
        if not queue:
            ctk.CTkLabel(self._queue_frame, text="Queue is empty", text_color="gray").pack(pady=20)
        else:
            for i, command in enumerate(queue):
                card = ctk.CTkFrame(self._queue_frame)
                card.pack(fill="x", pady=5)
                
                ctk.CTkLabel(card, text=f"#{i+1}", font=("Arial", 14, "bold")).pack(side="left", padx=10)
                ctk.CTkLabel(card, text=str(command)).pack(side="left", padx=10)
                
                ctk.CTkButton(card, text="Execute", width=70,
                             command=lambda cmd=command: self._execute_command(cmd)).pack(side="right", padx=5)
        
        for widget in self._history_list.winfo_children():
            widget.destroy()
        
        history = self._kitchen_service.queue.history
        for cmd in history:
            ctk.CTkLabel(self._history_list, text=str(cmd), text_color="#2ecc71").pack(fill="x", pady=2)
    
    def _execute_command(self, command):
        """Command'ni bajarish"""
        command.execute()
        self._kitchen_service.queue._history.append(command)
        self._kitchen_service.queue._queue.remove(command)
        self._refresh_queue()
    
    def _process_next(self):
        self._kitchen_service.process_next()
        self._refresh_queue()
    
    def _process_all(self):
        self._kitchen_service.process_all()
        self._refresh_queue()
    
    def _undo_last(self):
        self._kitchen_service.undo_last()
        self._refresh_queue()
