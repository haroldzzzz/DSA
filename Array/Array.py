import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class Array:
    def __init__(self, root):
        self.root = root
        self.root.title("FruitSaga Order System")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        self.init_database()
        self.create_widgets()
        self.load_inventory()
        
    def init_database(self):
        """Initialize SQLite database with tables"""
        self.conn = sqlite3.connect('fruit_ordering.db')
        self.cursor = self.conn.cursor()
        
        # Create Fruits table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS fruits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                stock_s INTEGER DEFAULT 0,
                stock_m INTEGER DEFAULT 0,
                stock_l INTEGER DEFAULT 0,
                price_s REAL DEFAULT 0,
                price_m REAL DEFAULT 0,
                price_l REAL DEFAULT 0
            )
        ''')
        
        # Create Orders table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                contact_no TEXT,
                order_date TEXT,
                total_price REAL
            )
        ''')
        
        # Create Order Items table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                fruit_name TEXT,
                size TEXT,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        ''')
        
        # Insert sample data if table is empty
        self.cursor.execute('SELECT COUNT(*) FROM fruits')
        if self.cursor.fetchone()[0] == 0:
            sample_fruits = [
                ('Apple', 50, 76, 94, 50, 75, 100),
                ('Mango', 43, 50, 74, 60, 85, 110),
                ('Pear', 12, 44, 90, 45, 70, 95),
                ('Orange', 50, 34, 7, 40, 65, 90)
            ]
            self.cursor.executemany('''
                INSERT INTO fruits (name, stock_s, stock_m, stock_l, price_s, price_m, price_l)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', sample_fruits)
        
        self.conn.commit()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title = tk.Label(self.root, text="Fruit Ordering System", 
                        font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title.pack(pady=10)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Inventory side
        left_frame = tk.LabelFrame(main_frame, text="Fruit Inventory", 
                                   font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Inventory table
        columns = ('Fruit', 'S', 'M', 'L')
        self.inventory_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=80, anchor='center')
        
        self.inventory_tree.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        inv_btn_frame = tk.Frame(left_frame, bg="white")
        inv_btn_frame.pack(pady=5, fill=tk.X)
        
        refresh_btn = tk.Button(inv_btn_frame, text="🔄 Refresh", 
                               command=self.load_inventory, bg="#3498db", fg="white",
                               font=("Arial", 10), cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        refill_btn = tk.Button(inv_btn_frame, text="📦 Refill Stock", 
                              command=self.refill_stock, bg="#f39c12", fg="white",
                              font=("Arial", 10), cursor="hand2")
        refill_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Order section
        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Customer info
        customer_frame = tk.LabelFrame(right_frame, text="Customer Information", 
                                      font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        customer_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(customer_frame, text="Name:", bg="white", font=("Arial", 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.customer_name = tk.Entry(customer_frame, width=30, font=("Arial", 10))
        self.customer_name.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(customer_frame, text="Contact:", bg="white", font=("Arial", 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.contact_no = tk.Entry(customer_frame, width=30, font=("Arial", 10))
        self.contact_no.grid(row=1, column=1, pady=5, padx=5)
        
        # Order items
        order_frame = tk.LabelFrame(right_frame, text="Order Items", 
                                   font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        order_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Fruit selection
        tk.Label(order_frame, text="Fruit:", bg="white", font=("Arial", 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.fruit_var = tk.StringVar()
        self.fruit_combo = ttk.Combobox(order_frame, textvariable=self.fruit_var, 
                                       values=[], state='readonly', width=15, font=("Arial", 10))
        self.fruit_combo.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(order_frame, text="Size:", bg="white", font=("Arial", 10)).grid(row=0, column=2, sticky='w', pady=5, padx=(10, 0))
        self.size_var = tk.StringVar(value="M")
        size_frame = tk.Frame(order_frame, bg="white")
        size_frame.grid(row=0, column=3, pady=5, padx=5)
        
        for size in ['S', 'M', 'L']:
            tk.Radiobutton(size_frame, text=size, variable=self.size_var, value=size,
                          bg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=2)
        
        tk.Label(order_frame, text="Quantity:", bg="white", font=("Arial", 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.quantity_var = tk.StringVar(value="1")
        quantity_spin = tk.Spinbox(order_frame, from_=1, to=100, textvariable=self.quantity_var, 
                                  width=10, font=("Arial", 10))
        quantity_spin.grid(row=1, column=1, pady=5, padx=5)
        
        add_btn = tk.Button(order_frame, text="➕ Add Item", command=self.add_item,
                          bg="#27ae60", fg="white", font=("Arial", 10, "bold"), cursor="hand2")
        add_btn.grid(row=1, column=2, columnspan=2, pady=5, padx=10)
        
        # Cart
        tk.Label(order_frame, text="Shopping Cart:", bg="white", 
                font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=4, sticky='w', pady=(10, 5))
        
        cart_columns = ('Fruit', 'Size', 'Qty', 'Price')
        self.cart_tree = ttk.Treeview(order_frame, columns=cart_columns, show='headings', height=6)
        
        for col in cart_columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=85, anchor='center')
        
        self.cart_tree.grid(row=3, column=0, columnspan=4, pady=5, sticky='ew')
        
        # Remove button
        remove_btn = tk.Button(order_frame, text="🗑️ Remove Selected", command=self.remove_item,
                             bg="#e74c3c", fg="white", font=("Arial", 9), cursor="hand2")
        remove_btn.grid(row=4, column=0, columnspan=2, pady=5, sticky='w')
        
        # Total
        self.total_var = tk.StringVar(value="Total: ₱0.00")
        total_label = tk.Label(order_frame, textvariable=self.total_var, bg="white",
                             font=("Arial", 12, "bold"), fg="#2c3e50")
        total_label.grid(row=4, column=2, columnspan=2, pady=5, sticky='e')
        
        # Buttons
        button_frame = tk.Frame(right_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X)
        
        place_order_btn = tk.Button(button_frame, text="✓ Place Order", command=self.place_order,
                                   bg="#2ecc71", fg="white", font=("Arial", 12, "bold"),
                                   cursor="hand2", padx=20, pady=8)
        place_order_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="↺ Clear Cart", command=self.clear_cart,
                            bg="#95a5a6", fg="white", font=("Arial", 12, "bold"),
                            cursor="hand2", padx=20, pady=8)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        receipt_btn = tk.Button(button_frame, text="📄 View Receipts", command=self.view_receipts,
                              bg="#9b59b6", fg="white", font=("Arial", 12, "bold"),
                              cursor="hand2", padx=20, pady=8)
        receipt_btn.pack(side=tk.LEFT, padx=5)
        
    def load_inventory(self):
        """Load inventory from database"""
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        self.cursor.execute('SELECT name, stock_s, stock_m, stock_l FROM fruits ORDER BY name')
        fruits = self.cursor.fetchall()
        
        fruit_names = []
        for fruit in fruits:
            # Replace 0 with "Empty"
            display_values = [fruit[0]]
            for stock in fruit[1:]:  # Stock S, M, L
                display_values.append("Empty" if stock == 0 else stock)
            
            self.inventory_tree.insert('', tk.END, values=display_values)
            fruit_names.append(fruit[0])
        
        self.fruit_combo['values'] = fruit_names
        if fruit_names:
            self.fruit_combo.current(0)
    
    def add_item(self):
        """Add item to cart"""
        fruit = self.fruit_var.get()
        size = self.size_var.get()
        
        try:
            quantity = int(self.quantity_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity")
            return
        
        if not fruit:
            messagebox.showerror("Error", "Please select a fruit")
            return
        
        # Get fruit info
        self.cursor.execute(f'''
            SELECT stock_{size.lower()}, price_{size.lower()} FROM fruits WHERE name = ?
        ''', (fruit,))
        result = self.cursor.fetchone()
        
        if not result:
            messagebox.showerror("Error", "Fruit not found")
            return
        
        stock, price = result
        
        if quantity > stock:
            messagebox.showerror("Error", f"Insufficient stock! Available: {stock}")
            return
        
        total_price = quantity * price
        self.cart_tree.insert('', tk.END, values=(fruit, size, quantity, f"₱{total_price:.2f}"))
        self.update_total()
        
    def remove_item(self):
        """Remove selected item from cart"""
        selected = self.cart_tree.selection()
        if selected:
            self.cart_tree.delete(selected)
            self.update_total()
        else:
            messagebox.showwarning("Warning", "Please select an item to remove")
    
    def update_total(self):
        """Update total price"""
        total = 0
        for item in self.cart_tree.get_children():
            values = self.cart_tree.item(item)['values']
            price_str = values[3].replace('₱', '')
            total += float(price_str)
        
        self.total_var.set(f"Total: ₱{total:.2f}")
    
    def clear_cart(self):
        """Clear all items from cart"""
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        self.update_total()
    
    def place_order(self):
        """Place the order and update database"""
        customer = self.customer_name.get().strip()
        contact = self.contact_no.get().strip()
        
        if not customer:
            messagebox.showerror("Error", "Please enter customer name")
            return
        
        if not self.cart_tree.get_children():
            messagebox.showerror("Error", "Cart is empty")
            return
        
        # Calculate total
        total = 0
        for item in self.cart_tree.get_children():
            values = self.cart_tree.item(item)['values']
            price_str = values[3].replace('₱', '')
            total += float(price_str)
        
        # Insert order
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO orders (customer_name, contact_no, order_date, total_price)
            VALUES (?, ?, ?, ?)
        ''', (customer, contact, order_date, total))
        order_id = self.cursor.lastrowid
        
        # Insert order items and update stock
        for item in self.cart_tree.get_children():
            values = self.cart_tree.item(item)['values']
            fruit, size, quantity = values[0], values[1], values[2]
            price_str = values[3].replace('₱', '')
            
            # Insert order item
            self.cursor.execute('''
                INSERT INTO order_items (order_id, fruit_name, size, quantity, price)
                VALUES (?, ?, ?, ?, ?)
            ''', (order_id, fruit, size, quantity, float(price_str)))
            
            # Update stock
            self.cursor.execute(f'''
                UPDATE fruits SET stock_{size.lower()} = stock_{size.lower()} - ?
                WHERE name = ?
            ''', (quantity, fruit))
        
        self.conn.commit()
        
        messagebox.showinfo("Success", f"Order placed successfully!\nOrder ID: {order_id}\nTotal: ₱{total:.2f}")
        
        # Clear form
        self.customer_name.delete(0, tk.END)
        self.contact_no.delete(0, tk.END)
        self.clear_cart()
        self.load_inventory()
    
    def view_receipts(self):
        """View order receipts in a new window"""
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Order Receipts")
        receipt_window.geometry("700x500")
        
        # Title
        tk.Label(receipt_window, text="Order History", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Orders list
        columns = ('Order ID', 'Customer', 'Contact', 'Date', 'Total')
        tree = ttk.Treeview(receipt_window, columns=columns, show='headings', height=15)
        
        tree.heading('Order ID', text='Order ID')
        tree.heading('Customer', text='Customer')
        tree.heading('Contact', text='Contact')
        tree.heading('Date', text='Date')
        tree.heading('Total', text='Total')
        
        tree.column('Order ID', width=80, anchor='center')
        tree.column('Customer', width=150, anchor='w')
        tree.column('Contact', width=120, anchor='w')
        tree.column('Date', width=150, anchor='center')
        tree.column('Total', width=100, anchor='e')
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load orders
        self.cursor.execute('SELECT id, customer_name, contact_no, order_date, total_price FROM orders ORDER BY id DESC')
        orders = self.cursor.fetchall()
        
        for order in orders:
            tree.insert('', tk.END, values=(
                order[0], 
                order[1], 
                order[2] or 'N/A', 
                order[3], 
                f"₱{order[4]:.2f}"
            ))
        
        # View details button
        def view_details():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select an order")
                return
            
            order_id = tree.item(selected[0])['values'][0]
            self.show_order_details(order_id)
        
        btn_frame = tk.Frame(receipt_window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="View Details", command=view_details,
                 bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                 cursor="hand2", padx=15, pady=5).pack()
    
    def refill_stock(self):
        """Open refill stock dialog"""
        # Check if a fruit is selected
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a fruit to refill")
            return
        
        # Get selected fruit name
        fruit_name = self.inventory_tree.item(selected[0])['values'][0]

        refill_window = tk.Toplevel(self.root)
        refill_window.title(f"Refill Stock - {fruit_name}")
        refill_window.geometry("400x350")
        refill_window.resizable(False, False)
        refill_window.configure(bg="white")
        refill_window.transient(self.root)
        refill_window.grab_set()
        
        # Header
        header = tk.Frame(refill_window, bg="#f39c12", pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, text=f"📦 Refill Stock", font=("Arial", 16, "bold"),
                bg="#f39c12", fg="white").pack()
        tk.Label(header, text=f"Fruit: {fruit_name}", font=("Arial", 12),
                bg="#f39c12", fg="white").pack()
        
        content = tk.Frame(refill_window, bg="white", padx=30, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(content, text="Enter refill amounts:", font=("Arial", 11, "bold"),
                bg="white").pack(pady=(0, 15))
        
        # Sizes ng Fruits
        entries = {}
        for size in ['S', 'M', 'L']:
            frame = tk.Frame(content, bg="white")
            frame.pack(fill=tk.X, pady=8)
            
            tk.Label(frame, text=f"Size {size}:", font=("Arial", 11),
                    bg="white", width=10, anchor='w').pack(side=tk.LEFT)
            
            entry = tk.Entry(frame, font=("Arial", 11), width=15)
            entry.insert(0, "0")
            entry.pack(side=tk.LEFT, padx=10)
            entries[size] = entry
            
            tk.Label(frame, text="units", font=("Arial", 10),
                    bg="white", fg="gray").pack(side=tk.LEFT)
        
        def apply_refill():
            try:
                # Get amounts
                amounts = {}
                for size, entry in entries.items():
                    amount = int(entry.get())
                    if amount < 0:
                        messagebox.showerror("Error", "Amounts must be positive")
                        return
                    amounts[size] = amount
                
                # Update database
                for size, amount in amounts.items():
                    if amount > 0:
                        self.cursor.execute(f'''
                            UPDATE fruits 
                            SET stock_{size.lower()} = stock_{size.lower()} + ?
                            WHERE name = ?
                        ''', (amount, fruit_name))
                
                self.conn.commit()
                
                total_added = sum(amounts.values())
                if total_added > 0:
                    messagebox.showinfo("Success", 
                                      f"Stock refilled successfully!\n\n"
                                      f"Size S: +{amounts['S']} units\n"
                                      f"Size M: +{amounts['M']} units\n"
                                      f"Size L: +{amounts['L']} units")
                    self.load_inventory()
                    refill_window.destroy()
                else:
                    messagebox.showwarning("Warning", "No stock was added")
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        # Button frame at the bottom
        btn_frame = tk.Frame(refill_window, bg="white", pady=15)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Center the buttons
        button_container = tk.Frame(btn_frame, bg="white")
        button_container.pack()
        
        tk.Button(button_container, text="✓ Apply Refill", command=apply_refill,
                 bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                 cursor="hand2", padx=25, pady=10, relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_container, text="✕ Cancel", command=refill_window.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                 cursor="hand2", padx=25, pady=10, relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
    
    def show_order_details(self, order_id):
        """Show detailed view of an order"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Order #{order_id} Details")
        detail_window.geometry("500x450") 
        detail_window.configure(bg="#f0f0f0")

        # Get order info
        self.cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = self.cursor.fetchone()
        
        # Header
        header = tk.Frame(detail_window, bg="#3498db", pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text=f"ORDER RECEIPT #{order_id}", font=("Arial", 16, "bold"),
                 bg="#3498db", fg="white").pack()
        
        # Info
        info_frame = tk.Frame(detail_window, bg="white", padx=20, pady=10)
        info_frame.pack(fill=tk.X, padx=10, pady=(10, 0)) # Added padx
        
        tk.Label(info_frame, text=f"Customer: {order[1]}", font=("Arial", 11),
                 bg="white", anchor='w').pack(fill=tk.X, pady=2)
        tk.Label(info_frame, text=f"Contact: {order[2] or 'N/A'}", font=("Arial", 11),
                 bg="white", anchor='w').pack(fill=tk.X, pady=2)
        tk.Label(info_frame, text=f"Date: {order[3]}", font=("Arial", 11),
                 bg="white", anchor='w').pack(fill=tk.X, pady=2)
        
        # Items
        tk.Label(detail_window, text="Order Items:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(10, 5))
        tree_frame = tk.Frame(detail_window, padx=10)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('Fruit', 'Size', 'Quantity', 'Price')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Load items
        self.cursor.execute('SELECT fruit_name, size, quantity, price FROM order_items WHERE order_id = ?', (order_id,))
        items = self.cursor.fetchall()
        
        for item in items:
            tree.insert('', tk.END, values=(item[0], item[1], item[2], f"₱{item[3]:.2f}"))
        
        # Total
        total_frame = tk.Frame(detail_window, bg="#ecf0f1", pady=10, padx=20, relief=tk.RIDGE, borderwidth=1)
        total_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 10)) 
        tk.Label(total_frame, text=f"TOTAL: ₱{order[4]:.2f}", font=("Arial", 14, "bold"),
                 bg="#ecf0f1", fg="#27ae60").pack(anchor='e', fill=tk.X)
    
    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = Array(root)
    root.mainloop()