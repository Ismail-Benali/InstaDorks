import tkinter as tk
from tkinter import messagebox, font as tkfont, ttk
import webbrowser
import os
import threading

# Colors and Styles
class AppStyle:
    PALETTE = {
        "background": "#F4F6F9",
        "primary": "#2C3E50",
        "secondary": "#3498DB",
        "accent": "#27AE60",
        "text_dark": "#1A2734",
        "text_light": "#FFFFFF",
        "card_bg": "#FFFFFF",
        "shadow": "#BDC3C7"
    }

    @classmethod
    def create_shadow_frame(cls, master):
        """Create a frame with shadow effect."""
        frame = tk.Frame(master, 
                         bg=cls.PALETTE["card_bg"], 
                         relief=tk.RAISED, 
                         borderwidth=0)
        frame.configure(highlightthickness=0)
        return frame

# Predefined Dork Types with Description
DORK_TYPES = {
    "Emails": {
        "query": 'site:instagram.com intext:"@gmail.com"',
        "description": "Search for email addresses associated with Instagram accounts."
    },
    "Hashtags": {
        "query": 'site:instagram.com "#{}"',
        "description": "Search using hashtags."
    },
    "External Links": {
        "query": 'site:instagram.com intext:"http"',
        "description": "Search using external links in posts."
    },
    "Profiles by Name": {
        "query": 'site:instagram.com "{}"',
        "description": "Search for profiles by name."
    },
    "Profiles": {
        "query": 'site:instagram.com "{}" OR "@" "{}"',
        "description": "Search for personal profiles associated with names on Instagram."
    },
    "Celebrities": {
        "query": 'site:instagram.com "{}"',
        "description": "Search for celebrity accounts."
    },
    "Phone Numbers": {
        "query": 'site:instagram.com intext:"phone number"',
        "description": "Search for phone numbers associated with Instagram accounts."
    },
    "Reels": {
        "query": 'site:instagram.com "reels" intext:"profile"',
        "description": "Search for short reels containing personal data such as names or account-related information."
    },
    "Tagged Photos": {
        "query": 'site:instagram.com "@" intext:"{}"',
        "description": "Search for tagged photos of people."
    },
    "Comments": {
        "query": 'site:instagram.com "comment" intext:"{}"',
        "description": "Search within comments containing people's names."
    },
    "Profile Bio": {
        "query": 'site:instagram.com "bio:" intext:"{}"',
        "description": "Search within profile bios containing people's names."
    },
    "Stories": {
        "query": 'site:instagram.com "stories" intext:"{}"',
        "description": "Search for stories containing people's names."
    },
    "Followers & Following": {
        "query": 'site:instagram.com "followers" intext:"{}"',
        "description": "Search for followers or followings associated with specific names."
    },
    "Locations": {
        "query": 'site:instagram.com "location:" intext:"{}"',
        "description": "Search for people who posted accounts associated with specific locations."
    },
    "Profile Photos": {
        "query": 'site:instagram.com "profile picture" intext:"{}"',
        "description": "Search for profile pictures of accounts associated with people."
    },
    "Followers’ Posts": {
        "query": 'site:instagram.com "post" intext:"{}" intext:"followers"',
        "description": "Search for posts made by people who follow accounts with a specific name."
    },
    "Tagged Stories": {
        "query": 'site:instagram.com "@" intext:"{}" intext:"stories"',
        "description": "Search for stories tagged with specific names."
    },
    "Profile Picture Update": {
        "query": 'site:instagram.com "update profile picture" intext:"{}"',
        "description": "Search for people who have recently updated their profile pictures."
    },
    "Mentioned in Bios": {
        "query": 'site:instagram.com "mentioned" intext:"{}"',
        "description": "Search for people mentioned in profile bios."
    },
    "Likes and Interactions": {
        "query": 'site:instagram.com "likes" intext:"{}"',
        "description": "Search for people who interacted with posts containing specific names."
    },
    "Tagged Events": {
        "query": 'site:instagram.com "event" intext:"{}"',
        "description": "Search for people associated with events they've been tagged in."
    },
    "Recent Posts": {
        "query": 'site:instagram.com "recent posts" intext:"{}"',
        "description": "Search for recent posts of people whose accounts contain specific names."
    },
    "Followers’ Locations": {
        "query": 'site:instagram.com "followers" intext:"{}"',
        "description": "Search for people following accounts with specific locations."
    }
}

class AdvancedDorksGenerator:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.create_widgets()
        self.history = []
        self.init_app_directory()

    def init_app_directory(self):
        """Create necessary app directories."""
        os.makedirs("data", exist_ok=True)

    def setup_window(self):
        """Set up the main window."""
        self.master.title("Instagram Dorks Generator Pro")
        self.master.geometry("850x650")
        self.master.configure(bg=AppStyle.PALETTE["background"])
        
        # Define fonts
        self.title_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12)
        self.body_font = tkfont.Font(family="Segoe UI", size=10)

    def create_widgets(self):
        # Main frame with shadow effect
        main_frame = AppStyle.create_shadow_frame(self.master)
        main_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor=tk.CENTER)

        # App title
        title_label = tk.Label(
            main_frame, 
            text="Instagram Google Dorks Generator", 
            font=self.title_font, 
            bg=AppStyle.PALETTE["card_bg"], 
            fg=AppStyle.PALETTE["primary"]
        )
        title_label.pack(pady=20)

        # Search frame
        search_frame = tk.Frame(main_frame, bg=AppStyle.PALETTE["card_bg"])
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        # Entry label
        tk.Label(
            search_frame, 
            text="Enter a keyword:", 
            font=self.subtitle_font, 
            bg=AppStyle.PALETTE["card_bg"], 
            fg=AppStyle.PALETTE["text_dark"]
        ).pack(side=tk.TOP, anchor='w')

        # Entry field
        self.keyword_entry = tk.Entry(
            search_frame, 
            width=50, 
            font=self.body_font,
            bg="white", 
            fg=AppStyle.PALETTE["text_dark"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=AppStyle.PALETTE["secondary"]
        )
        self.keyword_entry.pack(fill=tk.X, pady=5)
        tk.Frame(search_frame, height=1, bg=AppStyle.PALETTE["secondary"]).pack(fill=tk.X)

        # Dork types frame
        dork_types_frame = tk.Frame(main_frame, bg=AppStyle.PALETTE["card_bg"])
        dork_types_frame.pack(padx=20, pady=10, fill=tk.X)

        # Dork types title
        tk.Label(
            dork_types_frame, 
            text="Predefined Dork Types:", 
            font=self.subtitle_font, 
            bg=AppStyle.PALETTE["card_bg"], 
            fg=AppStyle.PALETTE["text_dark"]
        ).pack(side=tk.TOP, anchor='w')

        # Dropdown frame
        dropdown_frame = tk.Frame(dork_types_frame, bg=AppStyle.PALETTE["card_bg"])
        dropdown_frame.pack(fill=tk.X, pady=5)

        # Predefined Dork Types dropdown
        self.dork_type_var = tk.StringVar(dropdown_frame)
        self.dork_type_var.set("Choose a Dork Type")
        
        dork_type_menu = ttk.Combobox(
            dropdown_frame, 
            textvariable=self.dork_type_var, 
            values=list(DORK_TYPES.keys()),
            state="readonly",
            font=self.body_font
        )
        dork_type_menu.pack(fill=tk.X)
        dork_type_menu.bind('<<ComboboxSelected>>', self.on_dork_type_select)

        # Dork description space
        self.dork_description_var = tk.StringVar()
        description_label = tk.Label(
            dork_types_frame, 
            textvariable=self.dork_description_var,
            font=self.body_font,
            bg=AppStyle.PALETTE["card_bg"], 
            fg=AppStyle.PALETTE["secondary"],
            wraplength=700,
            justify=tk.RIGHT
        )
        description_label.pack(pady=5)

        # Result frame
        result_frame = tk.Frame(main_frame, bg=AppStyle.PALETTE["card_bg"])
        result_frame.pack(padx=20, pady=10, fill=tk.X)

        # Result title
        tk.Label(
            result_frame, 
            text="Generated Dork:", 
            font=self.subtitle_font, 
            bg=AppStyle.PALETTE["card_bg"], 
            fg=AppStyle.PALETTE["text_dark"]
        ).pack(side=tk.TOP, anchor='w')

        # Dork display space
        self.result_var = tk.StringVar()
        result_label = tk.Label(
            result_frame, 
            textvariable=self.result_var, 
            wraplength=700, 
            font=self.body_font,
            bg="white", 
            fg=AppStyle.PALETTE["text_dark"],
            relief=tk.FLAT,
            anchor='w',
            justify=tk.LEFT
        )
        result_label.pack(fill=tk.X, pady=5)
        tk.Frame(result_frame, height=1, bg=AppStyle.PALETTE["secondary"]).pack(fill=tk.X)

        # Button frame
        button_frame = tk.Frame(main_frame, bg=AppStyle.PALETTE["card_bg"])
        button_frame.pack(padx=20, pady=10, fill=tk.X)

        # Action buttons
        actions = [
            ("Generate Custom Dork", self.generate_custom_dork, AppStyle.PALETTE["secondary"]),
            ("Copy", self.copy_to_clipboard, AppStyle.PALETTE["accent"]),
            ("Search", self.search_dork, AppStyle.PALETTE["primary"])
        ]

        for text, command, color in actions:
            btn = tk.Button(
                button_frame, 
                text=text, 
                font=self.body_font,
                command=command,
                bg=color, 
                fg=AppStyle.PALETTE["text_light"],
                relief=tk.FLAT,
                activebackground=AppStyle.PALETTE["primary"]
            )
            btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    def on_dork_type_select(self, event=None):
        """Display Dork type description when selected."""
        selected_type = self.dork_type_var.get()
        if selected_type in DORK_TYPES:
            desc = DORK_TYPES[selected_type]["description"]
            self.dork_description_var.set(desc)

    def generate_custom_dork(self):
        """Generate a custom Dork based on user input and selected type."""
        keyword = self.keyword_entry.get().strip()
        selected_type = self.dork_type_var.get()

        if selected_type in DORK_TYPES and keyword:
            dork_template = DORK_TYPES[selected_type]["query"]
            dork = dork_template.format(keyword)
            self.result_var.set(dork)
            threading.Thread(target=self.save_history, args=(dork,), daemon=True).start()
        else:
            messagebox.showwarning("Error", "Please enter a keyword and select a Dork type.")

    def copy_to_clipboard(self):
        """Copy the Dork to clipboard."""
        dork = self.result_var.get()
        if dork:
            self.master.clipboard_clear()
            self.master.clipboard_append(dork)
            messagebox.showinfo("Copied", "Dork copied to clipboard!")

    def search_dork(self):
        """Search using the generated Dork."""
        dork = self.result_var.get()
        if dork:
            webbrowser.open(f"https://www.google.com/search?q={dork}")

    def save_history(self, dork):
        """Save the Dork history."""
        try:
            with open("data/dorks_history.txt", "a", encoding="utf-8") as file:
                file.write(f"{dork}\n")
        except Exception as e:
            print(f"Error saving history: {e}")

def main():
    root = tk.Tk()
    root.style = ttk.Style()
    root.style.theme_use('clam')  # Apply a clean theme
    app = AdvancedDorksGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
