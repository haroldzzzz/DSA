import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import math

class Graph:
    def __init__(self, root):
        self.root = root
        self.root.title("Fruit PathFinder")
        self.root.geometry("600x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database
        self.init_database()
        
        # Store data
        self.order_data = {
            'customer_name': '',
            'contact_no': '',
            'buyer_address': '',
            'fruits': [],
            'selected_stores': []
        }
        
        self.current_fruit_index = 0
        
        # Show main form
        self.show_order_form()

    def init_database(self):
        """Initialize SQLite database"""
        self.conn = sqlite3.connect('fruit_locations.db')
        self.cursor = self.conn.cursor()
        
        # Drop existing tables to recreate with correct schema
        self.cursor.execute('DROP TABLE IF EXISTS fruits')
        self.cursor.execute('DROP TABLE IF EXISTS locations')
        
        # Create locations table
        self.cursor.execute('''
            CREATE TABLE locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                image_path TEXT,
                rating REAL
            )
        ''')
        
        # Create fruits table
        self.cursor.execute('''
            CREATE TABLE fruits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location_id INTEGER,
                fruit_name TEXT NOT NULL,
                price REAL,
                stock INTEGER,
                distance REAL,
                FOREIGN KEY (location_id) REFERENCES locations (id)
            )
        ''')
        
        # Add sample data
        self.add_sample_data()
        
        self.conn.commit()

    def add_sample_data(self):
        """Add sample data - Real stores in Valenzuela, Paso de Blas"""
        sample_locations = [
            ("Prutas ni Lolo Diddy", "MacArthur Highway, Paso de Blas, Valenzuela City", "A", 4.8),
            ("EcoFruit Corner", "Gen. T. de Leon Street, Paso de Blas, Valenzuela City", "B", 4.5),
            ("Aroma Fresh Fruit Stand", "Paso de Blas Road, Paso de Blas, Valenzuela City", "C", 4.6),
            ("Fresh Basket Fruits", "McArthur Highway corner Maysan Road, Paso de Blas, Valenzuela City", "D", 4.7),
            ("VGC Bazaar", "E. Santos Road, Paso de Blas, Valenzuela City", "E", 4.2),
            ("Fruit Hub", "E. Santos Road, Paso de Blas, Valenzuela City", "F", 4.4),
            ("Puregold Paso De Blas", "Karuhatan Road, Paso de Blas, Valenzuela City", "G", 4.3),
            ("DALI Everyday Grocery", "Malinta Exit Road, Paso de Blas, Valenzuela City", "H", 4.1),
            ("Paso De Blas Market", "Market Road, Paso de Blas, Valenzuela City", "I", 4.5)
        ]
        
        for loc in sample_locations:
            self.cursor.execute('''
                INSERT INTO locations (name, address, image_path, rating)
                VALUES (?, ?, ?, ?)
            ''', loc)
            
        sample_fruits = [
            # Store A - Prutas ni Lolo Diddy
            (1, "Apple", 20.00, 150, 2.8),
            (1, "Banana", 55.00, 200, 2.8),
            (1, "Orange", 28.00, 120, 2.8),
            (1, "Mango", 115.00, 80, 2.8),
            (1, "Grape", 145.00, 60, 2.8),
            (1, "Strawberry", 195.00, 45, 2.8),
            # Store B - EcoFruit Corner
            (2, "Apple", 22.00, 130, 2.2),
            (2, "Watermelon", 75.00, 50, 2.2),
            (2, "Pineapple", 85.00, 70, 2.2),
            (2, "Orange", 30.00, 90, 2.2),
            # Store C - Aroma Fresh Fruit Stand
            (3, "Mango", 110.00, 100, 3.0),
            (3, "Banana", 50.00, 180, 3.0),
            (3, "Papaya", 65.00, 75, 3.0),
            (3, "Apple", 24.00, 110, 3.0),
            # Store D - Fresh Basket Fruits
            (4, "Apple", 18.00, 200, 1.5),
            (4, "Orange", 26.00, 150, 1.5),
            (4, "Grape", 140.00, 80, 1.5),
            (4, "Strawberry", 195.00, 40, 1.5),
            (4, "Mango", 108.00, 90, 1.5),
            # Store E - VGC Bazaar
            (5, "Apple", 25.00, 100, 2.0),
            (5, "Banana", 60.00, 140, 2.0),
            (5, "Orange", 32.00, 85, 2.0),
            (5, "Watermelon", 80.00, 45, 2.0),
            # Store F - Fruit Hub
            (6, "Grape", 150.00, 70, 1.8),
            (6, "Mango", 120.00, 65, 1.8),
            (6, "Pineapple", 90.00, 55, 1.8),
            (6, "Apple", 23.00, 125, 1.8),
            # Store G - Puregold Paso De Blas
            (7, "Apple", 21.00, 180, 3.5),
            (7, "Orange", 29.00, 130, 3.5),
            (7, "Banana", 58.00, 170, 3.5),
            (7, "Grape", 148.00, 65, 3.5),
            (7, "Papaya", 68.00, 60, 3.5),
            # Store H - DALI Everyday Grocery
            (8, "Apple", 26.00, 95, 4.0),
            (8, "Watermelon", 78.00, 40, 4.0),
            (8, "Orange", 31.00, 80, 4.0),
            (8, "Mango", 112.00, 70, 4.0),
            (8, "Strawberry", 200.00, 45, 4.0),
            # Store I - Paso De Blas Market
            (9, "Banana", 52.00, 190, 3.2),
            (9, "Mango", 105.00, 95, 3.2),
            (9, "Papaya", 62.00, 85, 3.2),
            (9, "Pineapple", 82.00, 65, 3.2),
            (9, "Apple", 19.00, 160, 3.2)
        ]
        
        for fruit in sample_fruits:
            self.cursor.execute('''
                INSERT INTO fruits (location_id, fruit_name, price, stock, distance)
                VALUES (?, ?, ?, ?, ?)
            ''', fruit)
            
        self.conn.commit()

    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_order_form(self):
        """Display the initial order form with reduced vertical space and compact size."""
        self.clear_window()
        self.root.geometry("600x600")
        
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', pady=15)
        title_frame.pack(fill='x')
        
        tk.Label(title_frame, text="Fruit Locator Order Form", 
                 font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white').pack()
        
        # Main Form
        form_frame = tk.Frame(self.root, bg='#f0f0f0')
        form_frame.pack(fill='x', padx=40, pady=15)
 
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=3)

        # Customer Name
        row_idx = 0
        tk.Label(form_frame, text="Customer Name:", font=('Arial', 11, 'bold'), 
                 bg='#f0f0f0').grid(row=row_idx, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(form_frame, width=30, font=('Arial', 11))
        self.name_entry.grid(row=row_idx, column=1, pady=5, padx=10, sticky='ew')
        
        # Contact Number
        row_idx += 1
        tk.Label(form_frame, text="Contact No:", font=('Arial', 11, 'bold'), 
                 bg='#f0f0f0').grid(row=row_idx, column=0, sticky='w', pady=5)
        self.contact_entry = tk.Entry(form_frame, width=30, font=('Arial', 11))
        self.contact_entry.grid(row=row_idx, column=1, pady=5, padx=10, sticky='ew')
        
        # Address of Buyer
        row_idx += 1
        tk.Label(form_frame, text="Address of Buyer:", font=('Arial', 11, 'bold'), 
                 bg='#f0f0f0').grid(row=row_idx, column=0, sticky='w', pady=5)
        self.address_entry = tk.Entry(form_frame, width=30, font=('Arial', 11))
        self.address_entry.grid(row=row_idx, column=1, pady=5, padx=10, sticky='ew')
        self.address_entry.insert(0, "Paso de Blas, Valenzuela City")
        
        # Fruits to Buy Label
        row_idx += 1
        tk.Label(form_frame, text="Fruits to Buy:", font=('Arial', 11, 'bold'), 
                 bg='#f0f0f0').grid(row=row_idx, column=0, sticky='nw', pady=10)
        
        # Fruits Checkboxes Frame
        fruits_frame = tk.Frame(form_frame, bg='#f0f0f0')
        fruits_frame.grid(row=row_idx, column=1, pady=10, padx=10, sticky='w')
        
        # Get available fruits
        self.cursor.execute('SELECT DISTINCT fruit_name FROM fruits ORDER BY fruit_name')
        available_fruits = [row[0] for row in self.cursor.fetchall()]
        
        # Configure the checkbox grid to use 3 columns
        self.fruit_vars = {}
        cols = 3 
        for i, fruit in enumerate(available_fruits):
            var = tk.BooleanVar()
            self.fruit_vars[fruit] = var
            cb = tk.Checkbutton(fruits_frame, text=fruit, variable=var,
                                 font=('Arial', 10), bg='#f0f0f0')
            cb.grid(row=i//cols, column=i%cols, sticky='w', padx=5, pady=2)
            
        # Locate Button
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(pady=15)
        
        locate_btn = tk.Button(btn_frame, text="🔍 Locate Best Stores",
                              font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                              command=self.process_order, cursor='hand2', 
                              padx=30, pady=10)
        locate_btn.pack()

    def process_order(self):
        """Process the order, validate inputs, and resize window."""
        # Validate inputs
        if not self.name_entry.get().strip():
            messagebox.showwarning("Missing Info", "Please enter customer name.")
            return
        
        if not self.contact_entry.get().strip():
            messagebox.showwarning("Missing Info", "Please enter contact number.")
            return
        
        if not self.address_entry.get().strip():
            messagebox.showwarning("Missing Info", "Please enter buyer's address.")
            return
        
        # Get selected fruits
        selected_fruits = [fruit for fruit, var in self.fruit_vars.items() if var.get()]
        
        if not selected_fruits:
            messagebox.showwarning("No Fruits", "Please select at least one fruit.")
            return
        
        # Store order data
        self.order_data['customer_name'] = self.name_entry.get().strip()
        self.order_data['contact_no'] = self.contact_entry.get().strip()
        self.order_data['buyer_address'] = self.address_entry.get().strip()
        self.order_data['fruits'] = selected_fruits
        self.order_data['selected_stores'] = []
    
        self.root.geometry("1000x700")
        
        # Start showing fruit details
        self.current_fruit_index = 0
        self.show_fruit_details()

    def show_fruit_details(self):
        """Show details for current fruit with map"""
        if self.current_fruit_index >= len(self.order_data['fruits']):
            # All fruits processed, show summary
            self.show_summary()
            return
        
        current_fruit = self.order_data['fruits'][self.current_fruit_index]
        
        # Get stores with this fruit
        self.cursor.execute('''
            SELECT l.id, l.name, l.address, l.image_path, f.price, f.distance
            FROM locations l
            JOIN fruits f ON l.id = f.location_id
            WHERE f.fruit_name = ?
        ''', (current_fruit,))
        
        stores = []
        for row in self.cursor.fetchall():
            store_id, name, address, image, price, distance = row
            stores.append({
                'id': store_id,
                'name': name,
                'address': address,
                'distance': distance,
                'price': price,
                'image': image
            })
        
        # Sort by distance
        stores.sort(key=lambda x: x['distance'])
        
        if not stores:
            messagebox.showinfo("Not Available",
                               f"{current_fruit} is not available in any store.")
            self.current_fruit_index += 1
            self.show_fruit_details()
            return
        
        # Display stores with map
        self.clear_window()
        
        # Title
        title_frame = tk.Frame(self.root, bg='#3498db', pady=15)
        title_frame.pack(fill='x')
        
        tk.Label(title_frame, text=f"FRUIT LOCATOR", 
                 font=('Arial', 20, 'bold'), bg='#3498db', fg='white').pack()
        tk.Label(title_frame, text=f"Finding: {current_fruit}",
                 font=('Arial', 14), bg='#3498db', fg='white').pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left side - Map
        left_frame = tk.Frame(content_frame, bg='white', relief='solid', borderwidth=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(left_frame, text="PATH VISUALIZATION", font=('Arial', 14, 'bold'), 
                 bg='white', fg='#2c3e50').pack(pady=5)
        tk.Label(left_frame, text="Line length reflects actual distance (km)", font=('Arial', 10), 
                 bg='white', fg='#3498db').pack(pady=(0, 10))
        
        # Canvas for map
        map_canvas = tk.Canvas(left_frame, bg='#e8f5e9', width=450, height=450)
        map_canvas.pack(padx=10, pady=10)
        
        # Draw path visualization 
        best_store = stores[0]
        self.draw_map(map_canvas, stores, best_store)
        
        # Right side - Details
        right_frame = tk.Frame(content_frame, bg='white', relief='solid', borderwidth=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # MyData section
        mydata_frame = tk.Frame(right_frame, bg='#e3f2fd', relief='solid', borderwidth=1)
        mydata_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(mydata_frame, text="MY DATA", font=('Arial', 12, 'bold'), 
                 bg='#e3f2fd').pack(pady=5)
        tk.Label(mydata_frame, text=f"Name: {self.order_data['customer_name']}",
                 font=('Arial', 10), bg='#e3f2fd', anchor='w').pack(fill='x', padx=10)
        tk.Label(mydata_frame, text=f"Address: {self.order_data['buyer_address']}",
                 font=('Arial', 10), bg='#e3f2fd', anchor='w').pack(fill='x', padx=10, pady=(0, 5))
        
        # Fruit info
        tk.Label(right_frame, text=current_fruit, font=('Arial', 16, 'bold'),
                 bg='white', fg='#e74c3c').pack(pady=10)
        
        # Store comparison table
        table_frame = tk.Frame(right_frame, bg='white')
        table_frame.pack(fill='x', padx=10, pady=5)
        
        # Headers
        headers = ['Store', 'Distance', 'Price']
        for col, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=('Arial', 11, 'bold'),
                      bg='#34495e', fg='white', width=12, relief='solid', borderwidth=1).grid(
                        row=0, column=col, sticky='ew')
        
        # Store rows
        for i, store in enumerate(stores[:5], start=1):
            bg_color = '#d5f4e6' if i == 1 else 'white'
            
            tk.Label(table_frame, text=store['name'], font=('Arial', 10),
                      bg=bg_color, anchor='w', padx=5, relief='solid', borderwidth=1).grid(
                        row=i, column=0, sticky='ew')
            tk.Label(table_frame, text=f"{store['distance']:.1f} km", font=('Arial', 10),
                      bg=bg_color, relief='solid', borderwidth=1).grid(
                        row=i, column=1, sticky='ew')
            tk.Label(table_frame, text=f"₱{store['price']:.2f}", font=('Arial', 10),
                      bg=bg_color, relief='solid', borderwidth=1).grid(
                        row=i, column=2, sticky='ew')
        
        # Best location info
        best_frame = tk.Frame(right_frame, bg='#27ae60', relief='solid', borderwidth=2)
        best_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(best_frame, text=f"✅ Best Location: {best_store['name']}",
                 font=('Arial', 12, 'bold'), bg='#27ae60', fg='white').pack(pady=5)
        tk.Label(best_frame, text=f"Distance: {best_store['distance']:.1f} km",
                 font=('Arial', 10), bg='#27ae60', fg='white').pack()
        tk.Label(best_frame, text=best_store['address'],
                 font=('Arial', 9), bg='#27ae60', fg='white', wraplength=350).pack(pady=(0, 5))
        
        # Save best store
        self.order_data['selected_stores'].append({
            'fruit': current_fruit,
            'store': best_store['name'],
            'distance': best_store['distance'],
            'price': best_store['price'],
            'address': best_store['address']
        })
        
        # Done button 
        done_btn = tk.Button(right_frame, text="✓ DONE",
                             font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                             command=self.next_fruit, cursor='hand2', 
                             padx=40, pady=8)
        done_btn.pack(fill='x', padx=10, pady=(5, 10)) 
        
    def draw_map(self, canvas, stores, best_store):
        """
        Draw map using a radial, scaled visualization with stable store placement.
        Visual distance (pixels) now accurately reflects the real distance (km).
        Store names are displayed as labels.
        """
        width = 450
        height = 450
        center_x, center_y = width // 2, height // 2
        
        # Fixed Angles for all 9 possible stores (A-I)
        store_angles = {
            'A': math.radians(0),   # Right
            'B': math.radians(40),  # Upper Right
            'C': math.radians(80),
            'D': math.radians(120), # Upper Left
            'E': math.radians(160), 
            'F': math.radians(200), # Left
            'G': math.radians(240), # Lower Left
            'H': math.radians(280),
            'I': math.radians(320)  # Lower Right
        }
        
        # Max Distance for Scaling
        max_real_distance = max(store['distance'] for store in stores)
        
        max_pixel_radius = 200
        if max_real_distance == 0:
            scale_factor = 0
        else:
            scale_factor = max_pixel_radius / (max_real_distance + 0.5) 
        
        # User location
        you_radius = 20
        canvas.create_oval(center_x - you_radius, center_y - you_radius, 
                           center_x + you_radius, center_y + you_radius,
                           fill='#27ae60', outline='#1e8449', width=3)
        canvas.create_text(center_x, center_y, text="You", 
                           font=('Arial', 10, 'bold'), fill='white')
                           
        # Draw paths
        for store in stores:
            store_name = store['name']
            store_letter = store['image'] 
            distance = store['distance']
            
            angle = store_angles.get(store_letter, math.radians(0))
            
            pixel_radius = distance * scale_factor
            
            store_x = center_x + pixel_radius * math.cos(angle)
            store_y = center_y + pixel_radius * math.sin(angle)
            
            
            is_best = (store_name == best_store['name'])
            
            # Draw path line
            line_color = '#27ae60' if is_best else '#bdc3c7'
            line_width = 4 if is_best else 2
            canvas.create_line(center_x, center_y, store_x, store_y, 
                               fill=line_color, width=line_width, dash=(5, 3))
            
            # Draw distance label on path
            mid_x = (center_x + store_x) / 2
            mid_y = (center_y + store_y) / 2
            
            # Distance background
            canvas.create_rectangle(mid_x-25, mid_y-10, mid_x+25, mid_y+10,
                                     fill='white', outline='#2c3e50')
            canvas.create_text(mid_x, mid_y, text=f"{distance:.1f}km",
                                 font=('Arial', 8, 'bold'), fill='#2c3e50')
            
            # Draw store circle
            circle_color = '#3498db' if is_best else '#5499c7'
            
            canvas.create_oval(store_x - 10, store_y - 10, store_x + 10, store_y + 10,
                               fill=circle_color, outline='#2c3e50', width=2)
            
            # Add Store Name Label
            label_x = store_x
            label_y = store_y
            
            if angle > math.radians(270) or angle < math.radians(90):
                anchor_pos = 'w'
                label_x += 15
            else:
                anchor_pos = 'e'
                label_x -= 15

            canvas.create_text(label_x, label_y, text=store_name,
                                 font=('Arial', 8, 'bold'), fill='#2c3e50', anchor=anchor_pos,
                                 width=80)


    def next_fruit(self):
        """Move to next fruit"""
        self.current_fruit_index += 1
        self.show_fruit_details()

    def show_summary(self):
        """Show order summary"""
        self.clear_window()
        self.root.geometry("1000x700") 
        
        # Title
        title_frame = tk.Frame(self.root, bg='#8e44ad', pady=20)
        title_frame.pack(fill='x')
        
        tk.Label(title_frame, text="📋 Order Summary",
                 font=('Arial', 24, 'bold'), bg='#8e44ad', fg='white').pack()
        
        # Customer info
        info_frame = tk.Frame(self.root, bg='#f0f0f0', pady=15)
        info_frame.pack(fill='x', padx=40)
        
        tk.Label(info_frame, text=f"Customer: {self.order_data['customer_name']}",
                 font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(anchor='w')
        tk.Label(info_frame, text=f"Contact: {self.order_data['contact_no']}",
                 font=('Arial', 12), bg='#f0f0f0').pack(anchor='w')
        tk.Label(info_frame, text=f"Address: {self.order_data['buyer_address']}",
                 font=('Arial', 12), bg='#f0f0f0').pack(anchor='w', pady=(0, 10))
        
        # Summary table
        summary_frame = tk.Frame(self.root, bg='#f0f0f0')
        summary_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Create treeview
        columns = ('Fruit', 'Distance', 'Price', 'Store', 'Address')
        tree = ttk.Treeview(summary_frame, columns=columns, show='headings', height=10)
        
        tree.heading('Fruit', text='Fruit')
        tree.heading('Distance', text='Distance (km)')
        tree.heading('Price', text='Price (₱)')
        tree.heading('Store', text='Best Store')
        tree.heading('Address', text='Address')
        
        tree.column('Fruit', width=120)
        tree.column('Distance', width=120)
        tree.column('Price', width=100)
        tree.column('Store', width=200)
        tree.column('Address', width=250)
        
        # Add data
        total_cost = 0
        for item in self.order_data['selected_stores']:
            tree.insert('', 'end', values=(
                item['fruit'],
                f"{item['distance']:.1f}",
                f"₱{item['price']:.2f}",
                item['store'],
                item['address']
            ))
            total_cost += item['price']
        
        scrollbar = ttk.Scrollbar(summary_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Total
        total_frame = tk.Frame(self.root, bg='#2c3e50', pady=15)
        total_frame.pack(fill='x', padx=40, pady=10)
        
        tk.Label(total_frame, text=f"Total Estimated Cost: ₱{total_cost:.2f}",
                 font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack()
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(pady=20)
        
        new_order_btn = tk.Button(btn_frame, text="📝 New Order",
                                  font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                                  command=self.show_order_form, cursor='hand2',
                                  padx=20, pady=8)
        new_order_btn.pack(side='left', padx=10)
        
        exit_btn = tk.Button(btn_frame, text="❌ Exit",
                            font=('Arial', 12, 'bold'), bg='#95a5a6', fg='white',
                            command=self.root.quit, cursor='hand2',
                            padx=20, pady=8)
        exit_btn.pack(side='left', padx=10)

    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = Graph(root)
    root.mainloop()