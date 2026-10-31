import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 

class LinkedListCircular:
    # --- DESIGN COLORS & CONFIG ---
    PRIMARY_COLOR = '#3498db'
    SECONDARY_COLOR = '#2ecc71'
    ACCENT_COLOR = '#e74c3c'
    BG_COLOR = '#f7f9fa'
    FRAME_BG = '#ecf0f1'
    TEXT_COLOR = '#2c3e50'

    def __init__(self, root):
        self.root = root
        self.root.title("FruitExplorer")
        self.root.geometry("550x550") 
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)
        
        self.setup_styles()
        
        # Store user selections
        self.selected_category = ""
        self.selected_fruit = ""
        self.selected_type = ""
        self.selected_nutrition = ""
        self.selected_benefit = ""
        
        self.category_var = tk.StringVar(root)
        self.fruit_var = tk.StringVar(root)
        
        # Category Descriptions
        self.category_descriptions = {
            "Citrus Fruits": "Citrus Fruits are juicy, have leathery rinds, and are famously rich in Vitamin C and antioxidants.",
            "Berry Fruits": "Berry Fruits are small, fleshy, and pulpy. They are high in fiber, water content, and various antioxidants like anthocyanins.",
            "Tropical Fruits": "Tropical Fruits grow in hot, humid climates and are known for their vibrant colors, intense sweetness, and high Vitamin A content.",
            "Pome Fruits": "Pome Fruits have a central core containing seeds enclosed in a membrane. They are typically rich in fiber and beneficial plant compounds.",
            "Drupe Fruits": "Drupe Fruits (or stone fruits) have a fleshy exterior surrounding a single, hardened pit or 'stone' that contains the seed."
        }
        
        # Fruit database
        self.fruit_data = { 
            "Citrus Fruits": {
                "Orange": {
                    "Valencia Orange": {
                        "Vitamin C": ["Boosts immune system", "Promotes skin health", "Aids iron absorption"],
                        "Fiber": ["Improves digestion", "Helps control blood sugar", "Promotes heart health"],
                        "Potassium": ["Regulates blood pressure", "Supports muscle function", "Maintains fluid balance"]
                    },
                    "Blood Orange": {
                        "Anthocyanins": ["Powerful antioxidant", "Reduces inflammation", "Protects heart health"],
                        "Vitamin C": ["Boosts immunity", "Collagen production", "Wound healing"],
                        "Folate": ["Supports cell growth", "DNA synthesis", "Red blood cell formation"]
                    }
                },
                "Lemon": {
                    "Eureka Lemon": {
                        "Vitamin C": ["Immune support", "Antioxidant protection", "Skin brightening"],
                        "Citric Acid": ["Aids digestion", "Prevents kidney stones", "Enhances mineral absorption"],
                        "Flavonoids": ["Anti-inflammatory", "Cancer prevention", "Heart protection"]
                    },
                    "Meyer Lemon": {
                        "Vitamin C": ["Strengthens immunity", "Fights free radicals", "Promotes healing"],
                        "Potassium": ["Heart health", "Nerve function", "Muscle contraction"],
                        "Vitamin B6": ["Brain development", "Mood regulation", "Energy metabolism"]
                    }
                },
                "Calamansi": {
                    "Philippine Lime": {
                        "Vitamin C": ["Immune booster", "Skin health", "Iron absorption"],
                        "Calcium": ["Bone strength", "Teeth health", "Muscle function"],
                        "Phosphorus": ["Energy production", "Bone formation", "Cell repair"]
                    }
                }
            },
            "Berry Fruits": {
                "Strawberry": {
                    "June Bearing": {
                        "Vitamin C": ["Immunity boost", "Skin elasticity", "Antioxidant"],
                        "Manganese": ["Bone health", "Metabolism support", "Wound healing"],
                        "Folate": ["Cell division", "Pregnancy health", "DNA synthesis"]
                    },
                    "Ever Bearing": {
                        "Anthocyanins": ["Heart protection", "Anti-aging", "Brain health"],
                        "Ellagic Acid": ["Cancer prevention", "Anti-inflammatory", "Skin protection"],
                        "Fiber": ["Digestive health", "Weight management", "Blood sugar control"]
                    }
                },
                "Blueberry": {
                    "Highbush": {
                        "Antioxidants": ["Brain function", "Anti-aging", "Disease prevention"],
                        "Vitamin K": ["Blood clotting", "Bone health", "Heart protection"],
                        "Fiber": ["Gut health", "Cholesterol reduction", "Satiety"]
                    }
                }
            },
            "Tropical Fruits": {
                "Mango": {
                    "Carabao Mango": {
                        "Vitamin A": ["Eye health", "Immune function", "Skin repair"],
                        "Vitamin C": ["Collagen synthesis", "Immunity", "Antioxidant"],
                        "Folate": ["Cell growth", "Pregnancy support", "Red blood cells"]
                    },
                    "Kent Mango": {
                        "Beta-carotene": ["Vision protection", "Immune support", "Cell growth"],
                        "Vitamin E": ["Antioxidant", "Skin health", "Cell protection"],
                        "Fiber": ["Digestive health", "Weight control", "Heart health"]
                    }
                },
                "Banana": {
                    "Cavendish": {
                        "Potassium": ["Blood pressure control", "Heart health", "Muscle function"],
                        "Vitamin B6": ["Brain health", "Mood regulation", "Energy production"],
                        "Fiber": ["Digestive health", "Fullness", "Blood sugar control"]
                    }
                }
            },
            "Pome Fruits": {
                "Apple": {
                    "Fuji Apple": {
                        "Fiber": ["Gut health", "Weight management", "Heart health"],
                        "Vitamin C": ["Immune support", "Antioxidant", "Collagen production"],
                        "Quercetin": ["Anti-inflammatory", "Brain protection", "Blood pressure control"]
                    },
                    "Gala Apple": {
                        "Polyphenols": ["Heart health", "Diabetes prevention", "Cancer protection"],
                        "Potassium": ["Blood pressure", "Stroke prevention", "Kidney health"],
                        "Vitamin K": ["Bone strength", "Blood clotting", "Heart health"]
                    }
                },
                "Pear": {
                    "Bartlett Pear": {
                        "Fiber": ["Digestive health", "Cholesterol reduction", "Weight control"],
                        "Copper": ["Red blood cell production", "Nerve health", "Immune function"],
                        "Vitamin C": ["Immunity", "Skin health", "Wound healing"]
                    }
                }
            },
            "Drupe Fruits": {
                "Cherry": {
                    "Sweet Cherry": {
                        "Melatonin": ["Sleep quality", "Antioxidant", "Inflammation reduction"],
                        "Vitamin C": ["Immune health", "Skin repair", "Iron absorption"],
                        "Potassium": ["Heart function", "Muscle health", "Fluid balance"]
                    },
                    "Sour Cherry": {
                        "Anthocyanins": ["Anti-inflammatory", "Pain relief", "Exercise recovery"],
                        "Vitamin A": ["Vision health", "Immune support", "Cell growth"],
                        "Fiber": ["Gut health", "Blood sugar control", "Heart health"]
                    }
                },
                "Peach": {
                    "Freestone Peach": {
                        "Vitamin A": ["Eye health", "Skin health", "Immune function"],
                        "Vitamin C": ["Antioxidant", "Collagen", "Immunity"],
                        "Potassium": ["Heart health", "Blood pressure", "Muscle function"]
                    }
                }
            }
        }
        
        # Initialize UI
        self.show_category_selection()

    def setup_styles(self):
        """Sets up custom ttk styles."""
        style = ttk.Style()
        style.theme_use('clam') 
        
        style.configure('TFrame', background=self.BG_COLOR)
        style.configure('Title.TLabel', font=('Verdana', 20, 'bold'), 
                        foreground=self.TEXT_COLOR, background=self.BG_COLOR)
        style.configure('TLabel', font=('Verdana', 12), 
                        foreground=self.TEXT_COLOR, background=self.BG_COLOR)
                        
        style.configure('TCombobox', font=('Verdana', 12), fieldbackground='white',
                        background=self.FRAME_BG, foreground=self.TEXT_COLOR)
        style.map('TCombobox', 
                  fieldbackground=[('readonly', 'white')],
                  selectbackground=[('readonly', self.PRIMARY_COLOR)],
                  selectforeground=[('readonly', 'white')])

        style.configure("TScrollbar", background=self.PRIMARY_COLOR, troughcolor=self.FRAME_BG)
        style.map("TScrollbar", background=[('active', self.ACCENT_COLOR)])
        
    def hover_enter(self, event, widget, color):
        """Custom hover effect for standard tk.Button."""
        widget.config(bg=color)

    def hover_leave(self, event, widget, color):
        """Custom un-hover effect for standard tk.Button."""
        widget.config(bg=color)
    
    def clear_window(self):
        """Destroys all widgets in the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # Category/Fruit Selection
    def show_category_selection(self):
        """Displays the category and fruit dropdowns using grid for tight alignment."""
        self.clear_window()
        
        self.category_var.set("") 
        self.fruit_var.set("")
        
        title = ttk.Label(self.root, text="Fruit Browser System", style='Title.TLabel')
        title.pack(pady=(25, 15))
        
        self.selection_frame = ttk.Frame(self.root, padding="15 15 15 15", relief=tk.RIDGE)
        self.selection_frame.pack(pady=10, padx=20, fill='x')
        self.selection_frame.grid_columnconfigure(0, weight=1)

        # Category Section
        category_label = ttk.Label(self.selection_frame, text="Select a Fruit Category:", 
                                     font=('Verdana', 12, 'bold'), foreground=self.TEXT_COLOR)
        category_label.grid(row=0, column=0, sticky='w', padx=10, pady=(5, 2))
        
        categories = sorted(list(self.fruit_data.keys()))
        
        category_menu = ttk.Combobox(self.selection_frame, textvariable=self.category_var, 
                                     values=categories, state='readonly', font=('Verdana', 12))
        category_menu.grid(row=1, column=0, sticky='ew', padx=10, pady=(0, 15))
        
        # Description Box
        self.description_label = tk.Label(self.selection_frame, text="", 
                                         font=('Verdana', 10, 'italic'), bg=self.FRAME_BG, 
                                         fg=self.TEXT_COLOR, wraplength=450, 
                                         justify='center', height=4, relief=tk.FLAT, 
                                         borderwidth=0, padx=10, pady=5)
        self.description_label.grid(row=2, column=0, sticky='ew', padx=10, pady=(5, 15))

        # Fruit Section
        self.fruit_label = ttk.Label(self.selection_frame, text="Select a Fruit:", 
                                      font=('Verdana', 12, 'bold'), foreground=self.TEXT_COLOR)
        self.fruit_label.grid(row=3, column=0, sticky='w', padx=10, pady=(5, 2))
        
        self.fruit_menu = ttk.Combobox(self.selection_frame, textvariable=self.fruit_var, 
                                       values=[], state='disabled', font=('Verdana', 12))
        self.fruit_menu.grid(row=4, column=0, sticky='ew', padx=10, pady=(0, 15))
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        button_frame.pack(pady=20)
        
        self.next_btn = tk.Button(button_frame, text="Next →", font=('Arial', 12, 'bold'),
                                 width=15, height=2, bg=self.SECONDARY_COLOR, fg='white', # Changed color to green
                                 activebackground='#27ae60', cursor='hand2', state='disabled',
                                 command=self.on_fruit_select)
        self.next_btn.pack(side='left', padx=15)
        
        self.category_var.trace_add('write', self.update_fruits_dropdown)
        self.fruit_var.trace_add('write', self.enable_next_button)

        self.category_var.set("Select a Category")


    def update_fruits_dropdown(self, *args):
        """Dynamically updates the fruit dropdown and displays the category description."""
        self.selected_category = self.category_var.get()
        
        if self.selected_category in self.fruit_data:
            description = self.category_descriptions.get(self.selected_category, "Description not available.")
            self.description_label.config(text=description, bg=self.FRAME_BG) 

            fruits = sorted(list(self.fruit_data[self.selected_category].keys()))
            
            self.fruit_var.set("Select a Fruit")
            self.fruit_menu['values'] = fruits
            self.fruit_menu['state'] = 'readonly'
            self.next_btn.config(state='disabled') 
        else:
            self.description_label.config(text="", bg=self.BG_COLOR)
            self.fruit_var.set("Select a Fruit")
            self.fruit_menu['values'] = []
            self.fruit_menu['state'] = 'disabled'
            self.next_btn.config(state='disabled')

    def enable_next_button(self, *args):
        """Enables the 'Next' button if a valid fruit is chosen."""
        selected_fruit_name = self.fruit_var.get()
        
        if selected_fruit_name in self.fruit_data.get(self.selected_category, {}):
            self.next_btn.config(state='normal')
        else:
            self.next_btn.config(state='disabled')

    def on_fruit_select(self):
        """Handles the 'Next' button press and proceeds to show fruit types."""
        fruit = self.fruit_var.get()
        if fruit in self.fruit_data.get(self.selected_category, {}):
            self.show_types(fruit)

    # Fruit Type Selection
    def show_types(self, fruit):
        """Displays buttons for selecting the specific type of the chosen fruit, using grid for centered buttons."""
        self.selected_fruit = fruit
        self.clear_window()
        
        title = ttk.Label(self.root, text=f"{fruit} Varieties", style='Title.TLabel')
        title.pack(pady=(25, 10))
        
        subtitle = ttk.Label(self.root, text="Select a Specific Type", font=('Verdana', 12, 'italic'))
        subtitle.pack(pady=5)
        
        frame = ttk.Frame(self.root, padding="15 15 15 15")
        frame.pack(pady=15, padx=20)
        
        fruit_types = list(self.fruit_data[self.selected_category][fruit].keys())
        
        for i, fruit_type in enumerate(fruit_types):
            btn = tk.Button(frame, text=fruit_type, font=('Verdana', 11, 'bold'),
                            width=22, height=2, bg=self.ACCENT_COLOR, fg='white',
                            activebackground='#c0392b', cursor='hand2',
                            command=lambda t=fruit_type: self.show_nutrition(t))
            btn.grid(row=i, column=0, pady=8, padx=10) 
            btn.bind("<Enter>", lambda e, b=btn: self.hover_enter(e, b, '#c0392b'))
            btn.bind("<Leave>", lambda e, b=btn: self.hover_leave(e, b, self.ACCENT_COLOR))
        
        back_btn = tk.Button(self.root, text="← Back to Category", font=('Arial', 10),
                              bg='#95a5a6', fg='white', width=18,
                              activebackground='#7f8c8d', command=self.show_category_selection)
        back_btn.pack(pady=20)
    
    # Nutrition Selection

    def show_nutrition(self, fruit_type):
        """Displays buttons for selecting the nutritional facts, using grid for centered buttons."""
        self.selected_type = fruit_type
        self.clear_window()
        
        title = ttk.Label(self.root, text=f"{fruit_type} Nutrition 💪", style='Title.TLabel')
        title.pack(pady=(25, 10))
        
        subtitle = ttk.Label(self.root, text="Select a Key Nutritional Fact", font=('Verdana', 12, 'italic'))
        subtitle.pack(pady=5)
        
        frame = ttk.Frame(self.root, padding="15 15 15 15")
        frame.pack(pady=15, padx=20)
        
        nutrition_data = self.fruit_data[self.selected_category][self.selected_fruit][fruit_type]
        
        for i, nutrition in enumerate(nutrition_data.keys()):
            btn_color = '#9b59b6'
            active_color = '#8e44ad'
            
            btn = tk.Button(frame, text=nutrition, font=('Verdana', 11, 'bold'),
                            width=22, height=2, bg=btn_color, fg='white',
                            activebackground=active_color, cursor='hand2',
                            command=lambda n=nutrition: self.show_benefits(n))
            btn.grid(row=i, column=0, pady=8, padx=10)
            btn.bind("<Enter>", lambda e, b=btn: self.hover_enter(e, b, active_color))
            btn.bind("<Leave>", lambda e, b=btn: self.hover_leave(e, b, btn_color))
        
        back_btn = tk.Button(self.root, text="← Back to Types", font=('Arial', 10),
                              bg='#95a5a6', fg='white', width=18,
                              activebackground='#7f8c8d', command=lambda: self.show_types(self.selected_fruit))
        back_btn.pack(pady=20)
    
    # Benefits

    def show_benefits(self, nutrition):
        """Displays the detailed benefits for the selected nutritional component, with buttons at the bottom."""
        self.selected_nutrition = nutrition
        self.clear_window()
        
        title = ttk.Label(self.root, text=f"{nutrition} Benefits 🌟", style='Title.TLabel')
        title.pack(pady=(25, 10))
        
        subtitle = ttk.Label(self.root, text=f"Key Benefits of {self.selected_fruit}'s {nutrition}", font=('Verdana', 12, 'italic'))
        subtitle.pack(pady=5)
        
        # Scrollable Area
        scroll_container = ttk.Frame(self.root, padding="15 15 15 15", relief=tk.SUNKEN)
        scroll_container.pack(fill="both", expand=True, padx=30, pady=10)

        canvas = tk.Canvas(scroll_container, bg=self.FRAME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=450)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        benefits = self.fruit_data[self.selected_category][self.selected_fruit][self.selected_type][nutrition]
        
        for i, benefit in enumerate(benefits, 1):
            benefit_frame = tk.Frame(scrollable_frame, bg='white', relief=tk.FLAT, borderwidth=1)
            benefit_frame.pack(pady=5, padx=10, fill='x')
            
            benefit_label = tk.Label(benefit_frame, text=f"✅ {benefit}",
                                     font=('Verdana', 10), bg='white', fg=self.TEXT_COLOR,
                                     wraplength=400, justify='left', padx=10, pady=5)
            benefit_label.pack(fill='x')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Button
        button_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        button_frame.pack(pady=15)
        
        back_btn = tk.Button(button_frame, text="← Back", font=('Arial', 11),
                             bg='#95a5a6', fg='white', width=12, height=2,
                             activebackground='#7f8c8d',
                             command=lambda: self.show_nutrition(self.selected_type))
        back_btn.pack(side='left', padx=10)

        done_btn = tk.Button(button_frame, text="View Summary", font=('Arial', 11, 'bold'),
                             bg=self.SECONDARY_COLOR, fg='white', width=15, height=2,
                             activebackground='#27ae60',
                             command=self.show_summary)
        done_btn.pack(side='left', padx=10)


    # Summary 

    def show_summary(self):
        """Displays the final summary of the user's selection."""
        self.clear_window()
        
        title = ttk.Label(self.root, text="Final Selection Summary 📋", style='Title.TLabel')
        title.pack(pady=(25, 15))
        
        canvas_container = ttk.Frame(self.root, padding="15 15 15 15", relief=tk.RIDGE)
        canvas_container.pack(fill="both", expand=True, padx=30, pady=10) 

        canvas = tk.Canvas(canvas_container, bg=self.FRAME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=450)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Summary data structure
        summary_data = [
            ("Category of Fruit:", self.selected_category),
            ("Fruit Picked:", self.selected_fruit),
            ("Type of Fruit:", self.selected_type),
            ("Nutrition Fact Focus:", self.selected_nutrition),
            ("Key Benefits:", ", ".join(self.fruit_data[self.selected_category][self.selected_fruit][self.selected_type][self.selected_nutrition]))
        ]

        for label, value in summary_data:
            item_frame = tk.Frame(scrollable_frame, bg='white', relief=tk.GROOVE, borderwidth=1)
            item_frame.pack(pady=8, padx=10, fill='x') 
            
            item_frame.grid_columnconfigure(0, weight=1)
            item_frame.grid_columnconfigure(1, weight=3)
            
            lbl = tk.Label(item_frame, text=label, font=('Verdana', 10, 'bold'),
                            bg='white', fg=self.PRIMARY_COLOR, anchor='w', justify='left')
            lbl.grid(row=0, column=0, sticky='nw', padx=(10, 5), pady=8)
            
            val = tk.Label(item_frame, text=value, font=('Verdana', 10),
                            bg='white', fg=self.TEXT_COLOR, wraplength=320, 
                            justify='left', anchor='w')
            val.grid(row=0, column=1, sticky='nw', padx=(5, 10), pady=8)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Button Frame 
        button_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        button_frame.pack(pady=15)
        
        new_search_btn = tk.Button(button_frame, text="Start New Search", font=('Arial', 11, 'bold'),
                                   bg=self.SECONDARY_COLOR, fg='white', width=18, height=2,
                                   activebackground='#27ae60', command=self.show_category_selection)
        new_search_btn.pack(side='left', padx=10)
    
    def __del__(self):
        """Ensures the database connection is closed when the application closes."""
        if hasattr(self, 'db_connection') and self.db_connection:
            self.db_connection.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = LinkedListCircular(root)
    root.mainloop()