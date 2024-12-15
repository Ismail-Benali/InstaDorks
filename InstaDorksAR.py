import tkinter as tk
from tkinter import messagebox, font as tkfont, ttk
import webbrowser
import os
import threading

# الألوان والأسلوب
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
        """إنشاء إطار بظل"""
        frame = tk.Frame(master, 
                         bg=cls.PALETTE["card_bg"], 
                         relief=tk.RAISED, 
                         borderwidth=0)
        frame.configure(highlightthickness=0)
        return frame

# الأنواع المسبقة للدورك مع الوصف
DORK_TYPES = {
    "البريد الإلكتروني": {
        "query": 'site:instagram.com intext:"@gmail.com"',
        "description": "البحث عن عناوين البريد الإلكتروني المرتبطة بحسابات إنستاجرام."
    },
    "الهاشتاجات": {
        "query": 'site:instagram.com "#{}"',
        "description": "البحث باستخدام الهاشتاجات."
    },
    "الروابط الخارجية": {
        "query": 'site:instagram.com intext:"http"',
        "description": "البحث باستخدام الروابط الخارجية في المنشورات."
    },
    "الحسابات بالاسم": {
        "query": 'site:instagram.com "{}"',
        "description": "البحث عن الحسابات بالاسم."
    },
    "الحسابات الشخصية": {
        "query": 'site:instagram.com "{}" OR "@" "{}"',
        "description": "البحث عن حسابات شخصية مرتبطة بالأسماء على إنستاجرام."
    },
    "المشاهير": {
        "query": 'site:instagram.com "{}"',
        "description": "البحث عن حسابات المشاهير."
    },
    "أرقام الهواتف": {
        "query": 'site:instagram.com intext:"phone number"',
        "description": "البحث عن أرقام الهواتف المرتبطة بحسابات إنستاجرام."
    },
    "الريلز": {
        "query": 'site:instagram.com "reels" intext:"profile"',
        "description": "البحث عن ريلز تحتوي على بيانات شخصية مثل الأسماء أو المعلومات المتعلقة بالحسابات."
    },
    "الصور المميزة": {
        "query": 'site:instagram.com "@" intext:"{}"',
        "description": "البحث عن الصور المميزة للأشخاص."
    },
    "التعليقات": {
        "query": 'site:instagram.com "comment" intext:"{}"',
        "description": "البحث في التعليقات التي تحتوي على أسماء الأشخاص."
    },
    "السير الذاتية": {
        "query": 'site:instagram.com "bio:" intext:"{}"',
        "description": "البحث داخل سير البروفايلات التي تحتوي على أسماء الأشخاص."
    },
    "القصص": {
        "query": 'site:instagram.com "stories" intext:"{}"',
        "description": "البحث في القصص التي تحتوي على أسماء الأشخاص."
    },
    "المتابعين والمتابعة": {
        "query": 'site:instagram.com "followers" intext:"{}"',
        "description": "البحث عن المتابعين أو الحسابات التي يتابعها أشخاص مرتبطون بأسماء معينة."
    },
    "المواقع": {
        "query": 'site:instagram.com "location:" intext:"{}"',
        "description": "البحث عن الأشخاص الذين نشروا حساباتهم المرتبطة بمواقع معينة."
    },
    "صور الحسابات الشخصية": {
        "query": 'site:instagram.com "profile picture" intext:"{}"',
        "description": "البحث عن صور الحسابات المرتبطة بالأشخاص."
    },
    "المنشورات والمتابعين": {
        "query": 'site:instagram.com "post" intext:"{}" intext:"followers"',
        "description": "البحث عن المنشورات التي نشرها الأشخاص الذين تحتوي حساباتهم على أسماء معينة."
    },
    "القصص المميزة": {
        "query": 'site:instagram.com "@" intext:"{}" intext:"stories"',
        "description": "البحث عن القصص المميزة التي تحتوي على أسماء معينة."
    },
    "تحديث الصور الشخصية": {
        "query": 'site:instagram.com "update profile picture" intext:"{}"',
        "description": "البحث عن الأشخاص الذين قاموا بتحديث صورهم الشخصية مؤخراً."
    },
    "الذكر في السير الذاتية": {
        "query": 'site:instagram.com "mentioned" intext:"{}"',
        "description": "البحث عن الأشخاص الذين تم ذكرهم في سير البروفايلات."
    },
    "الإعجابات والتفاعلات": {
        "query": 'site:instagram.com "likes" intext:"{}"',
        "description": "البحث عن الأشخاص الذين تفاعلوا مع منشورات تحتوي على أسماء معينة."
    },
    "الأحداث المميزة": {
        "query": 'site:instagram.com "event" intext:"{}"',
        "description": "البحث عن الأشخاص المرتبطين بالأحداث التي تم تمييزهم فيها."
    },
    "المنشورات الحديثة": {
        "query": 'site:instagram.com "recent posts" intext:"{}"',
        "description": "البحث عن المنشورات الحديثة للأشخاص الذين تحتوي حساباتهم على أسماء معينة."
    },
    "المتابعين بحسب الموقع": {
        "query": 'site:instagram.com "followers" intext:"{}"',
        "description": "البحث عن الأشخاص الذين يتابعون حسابات ذات مواقع معينة."
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
        """إنشاء مجلدات التطبيق اللازمة."""
        os.makedirs("data", exist_ok=True)

    def setup_window(self):
        """إعداد نافذة البرنامج الرئيسية."""
        self.master.title("مولّد دورك إنستاجرام برو")
        self.master.geometry("850x650")
        self.master.configure(bg=AppStyle.PALETTE["background"])
        self.master.option_add("*Right", "true")  # جعل النصوص جهة اليمين

        # تعاريف الخطوط
        self.title_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12)
        self.body_font = tkfont.Font(family="Segoe UI", size=10)

    def create_widgets(self):
        # الإطار الرئيسي بظل
        main_frame = AppStyle.create_shadow_frame(self.master)
        main_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor=tk.CENTER)

        # عنوان التطبيق
        title_label = tk.Label(
            main_frame, 
            text="مولد دورك إنستاجرام برو", 
            font=self.title_font, 
            bg=AppStyle.PALETTE["card_bg"], 
            fg=AppStyle.PALETTE["primary"]
        )
        title_label.pack(pady=20)

        # إطار البحث
        search_frame = tk.Frame(main_frame, bg=AppStyle.PALETTE["card_bg"])
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        # عنوان حقل الإدخال
        tk.Label(
            search_frame, 
            text="أدخل كلمة مفتاحية:", 
            font=self.subtitle_font, 
            bg=AppStyle.PALETTE["card_bg"], 
            fg=AppStyle.PALETTE["text_dark"],
            anchor='e'
        ).pack(side=tk.TOP, anchor='e')

        # حقل الإدخال
        self.keyword_entry = tk.Entry(
            search_frame, 
            width=50, 
            font=self.body_font,
            bg="white", 
            fg=AppStyle.PALETTE["text_dark"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=AppStyle.PALETTE["secondary"],
            justify=tk.RIGHT
        )
        self.keyword_entry.pack(fill=tk.X, pady=5)
        tk.Frame(search_frame, height=1, bg=AppStyle.PALETTE["secondary"]).pack(fill=tk.X)

        # إطار أنواع الدورك
        dork_types_frame = tk.Frame(main_frame, bg=AppStyle.PALETTE["card_bg"])
        dork_types_frame.pack(padx=20, pady=10, fill=tk.X)

        # عنوان أنواع الدورك
        tk.Label(
            dork_types_frame, 
            text="أنواع الدورك المسبقة:", 
            font=self.subtitle_font, 
            bg=AppStyle.PALETTE["card_bg"], 
            fg=AppStyle.PALETTE["text_dark"],
            anchor='e'
        ).pack(side=tk.TOP, anchor='e')

        # إطار القائمه المنسدلة
        dropdown_frame = tk.Frame(dork_types_frame, bg=AppStyle.PALETTE["card_bg"])
        dropdown_frame.pack(fill=tk.X, pady=5)

        # قائمة أنواع الدورك المسبقة
        self.dork_type_var = tk.StringVar(dropdown_frame)
        self.dork_type_var.set("اختر نوع الدورك")
        
        dork_type_menu = ttk.Combobox(
            dropdown_frame, 
            textvariable=self.dork_type_var, 
            values=list(DORK_TYPES.keys()),
            state="readonly",
            font=self.body_font,
            justify=tk.RIGHT
        )
        dork_type_menu.pack(fill=tk.X)
        dork_type_menu.bind('<<ComboboxSelected>>', self.on_dork_type_select)

        # مساحة الوصف للدورك
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

        # إطار النتيجة
        result_frame = tk.Frame(main_frame, bg=AppStyle.PALETTE["card_bg"])
        result_frame.pack(padx=20, pady=10, fill=tk.X)

        # عنوان النتيجة
        tk.Label(
            result_frame, 
            text="الدورك المولد:", 
            font=self.subtitle_font, 
            bg=AppStyle.PALETTE["card_bg"], 
            fg=AppStyle.PALETTE["text_dark"],
            anchor='e'
        ).pack(side=tk.TOP, anchor='e')

        # عرض الدورك المولد
        self.result_var = tk.StringVar()
        result_label = tk.Label(
            result_frame, 
            textvariable=self.result_var, 
            wraplength=700, 
            font=self.body_font,
            bg="white", 
            fg=AppStyle.PALETTE["text_dark"],
            relief=tk.FLAT,
            anchor='e',
            justify=tk.RIGHT
        )
        result_label.pack(fill=tk.X, pady=5)
        tk.Frame(result_frame, height=1, bg=AppStyle.PALETTE["secondary"]).pack(fill=tk.X)

        # إطار الأزرار
        button_frame = tk.Frame(main_frame, bg=AppStyle.PALETTE["card_bg"])
        button_frame.pack(padx=20, pady=10, fill=tk.X)

        # الأزرار
        actions = [
            ("إنشاء دورك مخصص", self.generate_custom_dork, AppStyle.PALETTE["secondary"]),
            ("نسخ", self.copy_to_clipboard, AppStyle.PALETTE["accent"]),
            ("بحث", self.search_dork, AppStyle.PALETTE["primary"])
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
        """إظهار وصف نوع الدورك عند الاختيار."""
        selected_type = self.dork_type_var.get()
        if selected_type in DORK_TYPES:
            desc = DORK_TYPES[selected_type]["description"]
            self.dork_description_var.set(desc)

    def generate_custom_dork(self):
        """إنشاء دورك مخصص بناءً على إدخال المستخدم ونوع الدورك المحدد."""
        keyword = self.keyword_entry.get().strip()
        selected_type = self.dork_type_var.get()

        if selected_type in DORK_TYPES and keyword:
            dork_template = DORK_TYPES[selected_type]["query"]
            dork = dork_template.format(keyword)
            self.result_var.set(dork)
            threading.Thread(target=self.save_history, args=(dork,), daemon=True).start()
        else:
            messagebox.showwarning("خطأ", "يرجى إدخال كلمة مفتاحية واختيار نوع الدورك.")

    def copy_to_clipboard(self):
        """نسخ الدورك إلى الحافظة."""
        dork = self.result_var.get()
        if dork:
            self.master.clipboard_clear()
            self.master.clipboard_append(dork)
            messagebox.showinfo("تم النسخ", "تم نسخ الدورك إلى الحافظة!")

    def search_dork(self):
        """البحث باستخدام الدورك المولد."""
        dork = self.result_var.get()
        if dork:
            webbrowser.open(f"https://www.google.com/search?q={dork}")

    def save_history(self, dork):
        """حفظ سجل الدورك."""
        try:
            with open("data/dorks_history.txt", "a", encoding="utf-8") as file:
                file.write(f"{dork}\n")
        except Exception as e:
            print(f"خطأ في حفظ السجل: {e}")

def main():
    root = tk.Tk()
    root.style = ttk.Style()
    root.style.theme_use('clam')  # استخدام نمط أنيق
    app = AdvancedDorksGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
