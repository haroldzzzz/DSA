import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from collections import deque
import calendar

def create_date_picker(parent, default_date):
    """Creates a basic date entry mechanism using a regular Entry for simplicity."""
    entry = tk.Entry(parent, font=('Arial', 10), width=12)
    entry.insert(0, default_date)
    
    def on_focus_in(event):
        if entry.get() == "YYYY-MM-DD":
            entry.delete(0, tk.END)
    
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, "YYYY-MM-DD")
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    return entry

class Queue:
    def __init__(self):
        self.conn = sqlite3.connect('tollgate.db')
        self.create_tables()
        self.setup_toll_rates()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Toll rates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS toll_rates (
                id INTEGER PRIMARY KEY,
                vehicle_type TEXT,
                class INTEGER,
                rate REAL
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                station INTEGER,
                plate_no TEXT,
                vehicle_type TEXT,
                class INTEGER,
                amount REAL,
                timestamp TEXT,
                status TEXT
            )
        ''')
        
        self.conn.commit()
    
    def setup_toll_rates(self):
        cursor = self.conn.cursor()
    
        cursor.execute('SELECT COUNT(*) FROM toll_rates')
        if cursor.fetchone()[0] == 0:
            # Sample toll rates
            rates = [
                ('Car', 1, 50.0),
                ('Car', 2, 75.0),
                ('Car', 3, 100.0),
                ('Motorcycle', 1, 20.0),
                ('Motorcycle', 2, 30.0),
                ('Motorcycle', 3, 40.0),
                ('Bus', 1, 100.0),
                ('Bus', 2, 150.0),
                ('Bus', 3, 200.0),
                ('Truck', 1, 120.0),
                ('Truck', 2, 180.0),
                ('Truck', 3, 250.0)
            ]
            
            cursor.executemany('''
                INSERT INTO toll_rates (vehicle_type, class, rate)
                VALUES (?, ?, ?)
            ''', rates)
            
            self.conn.commit()
    
    def get_toll_rate(self, vehicle_type, vclass):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT rate FROM toll_rates 
            WHERE vehicle_type = ? AND class = ?
        ''', (vehicle_type, vclass))
        
        result = cursor.fetchone()
        return result[0] if result else 0.0
    
    def add_transaction(self, station, plate_no, vehicle_type, vclass, amount, status='Completed'):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO transactions (station, plate_no, vehicle_type, class, amount, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (station, plate_no, vehicle_type, vclass, amount, timestamp, status))
        
        self.conn.commit()
    
    def get_station_summary(self, station):
        """Fetches all time transactions for a station."""
        return self.get_station_summary_filtered(station, None)

    def get_station_total(self, station):
        """Fetches all time total for a station."""
        return self.get_station_total_filtered(station, None)
        
    def get_station_summary_filtered(self, station, date_filter=None):
        """Fetches transactions for a station, optionally filtered by date (YYYY-MM-DD)."""
        cursor = self.conn.cursor()
        query = '''
            SELECT plate_no, vehicle_type, class, amount, timestamp
            FROM transactions
            WHERE station = ? AND status = 'Completed'
        '''
        params = [station]
        
        if date_filter:
            query += ' AND date(timestamp) = ?'
            params.append(date_filter)
            
        query += ' ORDER BY timestamp DESC'
        
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    
    def get_station_total_filtered(self, station, date_filter=None):
        """Calculates total revenue for a station, optionally filtered by date (YYYY-MM-DD)."""
        cursor = self.conn.cursor()
        query = '''
            SELECT SUM(amount) FROM transactions
            WHERE station = ? AND status = 'Completed'
        '''
        params = [station]
        
        if date_filter:
            query += ' AND date(timestamp) = ?'
            params.append(date_filter)
            
        cursor.execute(query, tuple(params))
        
        result = cursor.fetchone()
        return result[0] if result and result[0] else 0.0
    
    def get_all_rates(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT vehicle_type, class, rate FROM toll_rates ORDER BY vehicle_type, class')
        return cursor.fetchall()

class TollgateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tollgate Lane Management System")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        self.db = Queue()
        self.queues = {i: deque() for i in range(1, 6)}
        self.current_filter_date = None
        
        # Tollgate Masters
        self.tollgate_masters = {
            1: "Mark Harold Barela",
            2: "Michael Angelo Saluria",
            3: "Justin Leoj Quimpo",
            4: "Qin Shi Huang",
            5: "Simo Hayha"
        }
        
        self.show_main_menu()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#2c3e50')
        frame.pack(expand=True)
        
        title = tk.Label(frame, text="Tollgate Management System", 
                         font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=30)
        
        btn_employee = tk.Button(frame, text="EMPLOYEE", command=self.show_station_selection,
                                 font=('Arial', 16), bg='#3498db', fg='white',
                                 width=20, height=2, cursor='hand2')
        btn_employee.pack(pady=15)
        
        btn_manager = tk.Button(frame, text="MANAGER", command=lambda: self.show_manager_view(),
                                font=('Arial', 16), bg='#27ae60', fg='white',
                                width=20, height=2, cursor='hand2')
        btn_manager.pack(pady=15)
    
    def show_station_selection(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#2c3e50')
        frame.pack(expand=True)
        
        title = tk.Label(frame, text="Select Station", 
                         font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=20)
        
        for i in range(1, 6):
            btn = tk.Button(frame, text=f"Station {i}", 
                            command=lambda s=i: self.show_employee_view(s),
                            font=('Arial', 14), bg='#3498db', fg='white',
                            width=15, height=2, cursor='hand2')
            btn.pack(pady=10)
        
        btn_back = tk.Button(frame, text="Back", command=self.show_main_menu,
                            font=('Arial', 12), bg='#e74c3c', fg='white',
                            width=10, cursor='hand2')
        btn_back.pack(pady=20)
    
    def show_employee_view(self, station):
        self.clear_window()
        self.current_station = station
     
        master_name = self.tollgate_masters.get(station, "N/A")
    
        top_frame = tk.Frame(self.root, bg='#2c3e50')
        top_frame.pack(fill='x', padx=10, pady=10)
        
        title_text = f"Station {station} - Lane Master: {master_name}"
        title = tk.Label(top_frame, text=title_text, 
                         font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white')
        title.pack(side='left', padx=10)
        
        btn_back = tk.Button(top_frame, text="Back", command=self.show_station_selection,
                            font=('Arial', 10), bg='#e74c3c', fg='white', cursor='hand2')
        btn_back.pack(side='right', padx=10)
        
        content_frame = tk.Frame(self.root, bg='#34495e')
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        left_panel = tk.Frame(content_frame, bg='#34495e')
        left_panel.pack(side='left', fill='both', expand=True, padx=5)
        
        tk.Label(left_panel, text="Toll Rates", font=('Arial', 14, 'bold'),
                 bg='#34495e', fg='white').pack(pady=10)
        
        # Toll rates table
        rate_frame = tk.Frame(left_panel, bg='white')
        rate_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tree_rates = ttk.Treeview(rate_frame, columns=('Type', 'Class', 'Rate'), 
                                  show='headings', height=15)
        tree_rates.heading('Type', text='Vehicle Type')
        tree_rates.heading('Class', text='Class')
        tree_rates.heading('Rate', text='Rate (₱)')
        
        tree_rates.column('Type', width=120)
        tree_rates.column('Class', width=80)
        tree_rates.column('Rate', width=100)
        
        # toll rates
        rates = self.db.get_all_rates()
        for rate in rates:
            tree_rates.insert('', 'end', values=(rate[0], rate[1], f"₱{rate[2]:.2f}"))
        
        tree_rates.pack(fill='both', expand=True)
        
        # Queuing Process
        right_panel = tk.Frame(content_frame, bg='#34495e')
        right_panel.pack(side='right', fill='both', expand=True, padx=5)
        
        tk.Label(right_panel, text="Queue Management", font=('Arial', 14, 'bold'),
                 bg='#34495e', fg='white').pack(pady=10)
        
        # Input form
        form_frame = tk.Frame(right_panel, bg='#ecf0f1', relief='raised', bd=2)
        form_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(form_frame, text="License Plate:", bg='#ecf0f1', 
                 font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.entry_plate = tk.Entry(form_frame, font=('Arial', 10), width=20)
        self.entry_plate.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Vehicle Type:", bg='#ecf0f1',
                 font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.combo_type = ttk.Combobox(form_frame, values=['Car', 'Motorcycle', 'Bus', 'Truck'],
                                         state='readonly', font=('Arial', 10), width=18)
        self.combo_type.grid(row=1, column=1, padx=10, pady=5)
        self.combo_type.current(0)
        
        tk.Label(form_frame, text="Class:", bg='#ecf0f1',
                 font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.combo_class = ttk.Combobox(form_frame, values=[1, 2, 3],
                                         state='readonly', font=('Arial', 10), width=18)
        self.combo_class.grid(row=2, column=1, padx=10, pady=5)
        self.combo_class.current(0)
        
        # Buttons
        btn_frame = tk.Frame(right_panel, bg='#34495e')
        btn_frame.pack(fill='x', padx=5, pady=10)
        
        tk.Button(btn_frame, text="Add to Queue", command=self.add_to_queue,
                  bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                  cursor='hand2').pack(side='left', padx=5, expand=True, fill='x')
        
        tk.Button(btn_frame, text="Next in Queue", command=self.next_in_queue,
                  bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                  cursor='hand2').pack(side='left', padx=5, expand=True, fill='x')
        
        tk.Button(btn_frame, text="Complete Transaction", command=self.complete_transaction,
                  bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                  cursor='hand2').pack(side='left', padx=5, expand=True, fill='x')
        
        # Queue display
        queue_frame = tk.Frame(right_panel, bg='white')
        queue_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Label(queue_frame, text="Current Queue", font=('Arial', 12, 'bold'),
                 bg='white').pack(pady=5)
        
        self.queue_listbox = tk.Listbox(queue_frame, font=('Arial', 10), height=10)
        self.queue_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Current vehicle frame
        self.current_frame = tk.Frame(right_panel, bg='#ecf0f1', relief='raised', bd=2)
        self.current_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(self.current_frame, text="Current Vehicle: None", 
                 font=('Arial', 11, 'bold'), bg='#ecf0f1').pack(pady=10)
        
        self.current_vehicle = None
        self.update_queue_display()
    
    def add_to_queue(self):
        plate = self.entry_plate.get().strip().upper()
        vehicle_type = self.combo_type.get()
        vclass = int(self.combo_class.get())
        
        if not plate:
            messagebox.showwarning("Warning", "Please enter license plate number")
            return
        
        vehicle_data = {
            'plate': plate,
            'type': vehicle_type,
            'class': vclass
        }
        
        self.queues[self.current_station].append(vehicle_data)
        
        # Clear inputs
        self.entry_plate.delete(0, tk.END)
        self.combo_type.current(0)
        self.combo_class.current(0)
        
        self.update_queue_display()
        messagebox.showinfo("Success", f"Vehicle {plate} added to queue")
    
    def next_in_queue(self):
        if len(self.queues[self.current_station]) == 0:
            messagebox.showinfo("Info", "Queue is empty")
            return
        
        self.current_vehicle = self.queues[self.current_station].popleft()
        self.update_queue_display()
    
        for widget in self.current_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.current_frame, 
                 text=f"Current Vehicle: {self.current_vehicle['plate']}", 
                 font=('Arial', 11, 'bold'), bg='#ecf0f1').pack(pady=5)
        tk.Label(self.current_frame, 
                 text=f"Type: {self.current_vehicle['type']} | Class: {self.current_vehicle['class']}", 
                 font=('Arial', 10), bg='#ecf0f1').pack(pady=5)
        
        rate = self.db.get_toll_rate(self.current_vehicle['type'], self.current_vehicle['class'])
        tk.Label(self.current_frame, 
                 text=f"Amount: ₱{rate:.2f}", 
                 font=('Arial', 12, 'bold'), bg='#ecf0f1', fg='#27ae60').pack(pady=5)
    
    def complete_transaction(self):
        if not self.current_vehicle:
            messagebox.showwarning("Warning", "No vehicle in processing")
            return
        
        rate = self.db.get_toll_rate(self.current_vehicle['type'], self.current_vehicle['class'])
        
        self.db.add_transaction(
            self.current_station,
            self.current_vehicle['plate'],
            self.current_vehicle['type'],
            self.current_vehicle['class'],
            rate
        )
        messagebox.showinfo("Success", 
                             f"Transaction completed!\nAmount: ₱{rate:.2f}")
        
        self.current_vehicle = None
    
        for widget in self.current_frame.winfo_children():
            widget.destroy()
        tk.Label(self.current_frame, text="Current Vehicle: None", 
                 font=('Arial', 11, 'bold'), bg='#ecf0f1').pack(pady=10)
    
    def update_queue_display(self):
        self.queue_listbox.delete(0, tk.END)
        
        for i, vehicle in enumerate(self.queues[self.current_station], 1):
            display_text = f"{i}. {vehicle['plate']} - {vehicle['type']} (Class {vehicle['class']})"
            self.queue_listbox.insert(tk.END, display_text)
    
    def show_manager_view(self, date_filter=None):
        self.clear_window()
        self.current_filter_date = date_filter
        
        total_remittance = 0 
        
        grand_total_frame = tk.Frame(self.root, bg='#2ecc71', relief='raised', bd=3)
        grand_total_frame.pack(fill='x', padx=10, pady=(0, 10), side=tk.BOTTOM) 
        
        self.grand_total_label = tk.Label(grand_total_frame, 
                                          text="Calculating...", 
                                          font=('Arial', 18, 'bold'), 
                                          bg='#2ecc71', 
                                          fg='white')
        self.grand_total_label.pack(pady=20)

        top_frame = tk.Frame(self.root, bg='#2c3e50')
        top_frame.pack(fill='x', padx=10, pady=10)
        
        title_text = "Manager Dashboard - Station Summary"
        if date_filter:
             title_text += f" (Filtered: {date_filter})"
        else:
             title_text += f" (All Time)"
             
        title = tk.Label(top_frame, text=title_text, 
                         font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white')
        title.pack(side='left')
        
        btn_back = tk.Button(top_frame, text="Back", command=self.show_main_menu,
                            font=('Arial', 10), bg='#e74c3c', fg='white', cursor='hand2')
        btn_back.pack(side='right')

        filter_frame = tk.Frame(self.root, bg='#bdc3c7')
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(filter_frame, text="Filter by Date (YYYY-MM-DD):", bg='#bdc3c7', 
                 font=('Arial', 10, 'bold')).pack(side='left', padx=(10, 5))
        
        self.date_entry = create_date_picker(filter_frame, datetime.now().strftime('%Y-%m-%d') if date_filter is None else date_filter)
        self.date_entry.pack(side='left', padx=5)
        
        # Filter Button
        btn_filter = tk.Button(filter_frame, text="Filter", 
                               command=self.apply_date_filter,
                               font=('Arial', 10, 'bold'), bg='#3498db', fg='white', cursor='hand2')
        btn_filter.pack(side='left', padx=5)
        
        # Clear Button
        btn_clear = tk.Button(filter_frame, text="Clear Filter (All Time)", 
                              command=lambda: self.show_manager_view(date_filter=None),
                              font=('Arial', 10), bg='#f39c12', fg='white', cursor='hand2')
        btn_clear.pack(side='left', padx=5)
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=(5, 5))
        
        # Calculations
        for station in range(1, 6):

            station_frame = tk.Frame(notebook, bg='white')
            notebook.add(station_frame, text=f"Station {station}")
            
            master_name = self.tollgate_masters.get(station, "N/A")
            tk.Label(station_frame, text=f"Station {station} Summary (Lane Master: {master_name})", 
                     font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
            
            tree_frame = tk.Frame(station_frame)
            tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            tree = ttk.Treeview(tree_frame, 
                                 columns=('Plate', 'Type', 'Class', 'Amount', 'Time'), 
                                 show='headings', height=15)
            
            tree.heading('Plate', text='Plate No.')
            tree.heading('Type', text='Vehicle Type')
            tree.heading('Class', text='Class')
            tree.heading('Amount', text='Amount')
            tree.heading('Time', text='Timestamp')
            
            tree.column('Plate', width=120)
            tree.column('Type', width=120)
            tree.column('Class', width=80)
            tree.column('Amount', width=100)
            tree.column('Time', width=180)
            
            scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side='right', fill='y')
            tree.pack(fill='both', expand=True)
            
            transactions = self.db.get_station_summary_filtered(station, date_filter)
            for trans in transactions:
                tree.insert('', 'end', values=(trans[0], trans[1], trans[2], f"₱{trans[3]:.2f}", trans[4]))
            
            total = self.db.get_station_total_filtered(station, date_filter)
            total_remittance += total
            
            total_frame = tk.Frame(station_frame, bg='#ecf0f1', relief='raised', bd=2)
            total_frame.pack(fill='x', padx=10, pady=10)
            
            tk.Label(total_frame, text=f"Total Collection: ₱{total:.2f}", 
                     font=('Arial', 14, 'bold'), bg='#ecf0f1', fg='#27ae60').pack(pady=10)
        
        # Toal Remittance
        self.grand_total_label.config(text=f"Total Remittance (All Stations): ₱{total_remittance:.2f}")

    def apply_date_filter(self):
        date_str = self.date_entry.get().strip()
        
        if date_str == "YYYY-MM-DD":
            messagebox.showwarning("Warning", "Please enter a valid date in YYYY-MM-DD format.")
            return

        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            self.show_manager_view(date_filter=date_str)
        except ValueError:
            messagebox.showwarning("Invalid Date", "The date must be in YYYY-MM-DD format (e.g., 2025-12-14).")

if __name__ == "__main__":
    root = tk.Tk()
    app = TollgateApp(root)
    root.mainloop()