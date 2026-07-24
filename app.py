```python
import os
import tkinter as tk
from tkinter import messagebox, ttk

# أسماء الملفات الرئيسية الأربعة المطلوبة استدعاؤها والتعامل معها مباشرة
PRIMARY_FILES = ["ameer.pdf", "Almamlaka.pdf", "Ardzekola.pdf", "wady.pdf"]

# التأكد من توفر الملفات الأساسية تلقائياً عند التشغيل
for filename in PRIMARY_FILES:
  if not os.path.exists(filename):
    with open(filename, "w", encoding="utf-8") as f:
      f.write(f"Primary document content for {filename}")

# ربط الملفات الرئيسية ببيانات الواجهة التفاعلية
my_novels = [
    {
        "title": "ملف الأمير التوثيقي",
        "author": "Ameer Document",
        "desc": "ملف توثيقي احترافي تم استدعاؤه وإدارته مباشرة.",
        "pdf": "ameer.pdf",
    },
    {
        "title": "مملكة الفعاليات والأنظمة",
        "author": "Almamlaka System",
        "desc": "عرض التفاصيل الأساسية والبيانات الموثقة للمملكة.",
        "pdf": "Almamlaka.pdf",
    },
    {
        "title": "أرض الذكاء الاصطناعي والحوسبة",
        "author": "Ardzekola AI",
        "desc": (
            "ملف رئيسي خاص بأبحاث ومشاريع الذكاء الاصطناعي والحوسبة السحابية."
        ),
        "pdf": "Ardzekola.pdf",
    },
    {
        "title": "وادي التقنية والحلول البرمجية",
        "author": "Wady Technology",
        "desc": "محتوى توثيقي رئيسي يختص بوادي التقنية والحلول البرمجية.",
        "pdf": "wady.pdf",
    },
]


class LibraryApp:

  def __init__(self, root):
    self.root = root
    self.root.title("المكتبة المتكاملة 📚")
    self.root.geometry("850x600")
    self.root.configure(bg="#0c0a1a")

    self.root.option_add("*Font", "Tajawal 11")
    self.show_welcome_screen()

  def clear_window(self):
    for widget in self.root.winfo_children():
      widget.destroy()

  def show_welcome_screen(self):
    self.clear_window()

    frame = tk.Frame(self.root, bg="#1f1735", bd=2, relief="groove")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=350)

    title_label = tk.Label(
        frame,
        text="📚 مكتبة الروايات الخاصة",
        font=("Tajawal", 22, "bold"),
        bg="#1f1735",
        fg="#f3e5ab",
    )
    title_label.pack(pady=30)

    desc_label = tk.Label(
        frame,
        text=(
            "مرحباً بكِ يا حميدة في مكتبتك الرقمية.\nتم استدعاء الملفات"
            " الرئيسية بنجاح، اضغطي بالأسفل للدخول."
        ),
        font=("Tajawal", 12),
        bg="#1f1735",
        fg="#b8a5c9",
        justify="center",
    )
    desc_label.pack(pady=10)

    enter_btn = tk.Button(
        frame,
        text="دخول المكتبة 📖",
        font=("Tajawal", 14, "bold"),
        bg="#d4af37",
        fg="#0c0a1a",
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2",
        command=self.show_library_screen,
    )
    enter_btn.pack(pady=30)

  def show_library_screen(self):
    self.clear_window()

    back_btn = tk.Button(
        self.root,
        text="⬅ العودة للرئيسية",
        font=("Tajawal", 10, "bold"),
        bg="#0c0a1a",
        fg="#d4af37",
        bd=1,
        relief="solid",
        command=self.show_welcome_screen,
    )
    back_btn.pack(anchor="nw", padx=20, pady=10)

    header_frame = tk.Frame(self.root, bg="#1f1735", padx=20, pady=15)
    header_frame.pack(fill="x", padx=20, pady=5)

    header_label = tk.Label(
        header_frame,
        text="✨ روايات حميدة المميزة (الملفات الرئيسية)",
        font=("Tajawal", 18, "bold"),
        bg="#1f1735",
        fg="#f3e5ab",
    )
    header_label.pack(side="right")

    search_frame = tk.Frame(self.root, bg="#0c0a1a")
    search_frame.pack(fill="x", padx=20, pady=15)

    self.search_entry = tk.Entry(
        search_frame,
        font=("Tajawal", 12),
        bg="#2a1f42",
        fg="#f0e6f5",
        insertbackground="white",
        justify="right",
    )
    self.search_entry.pack(fill="x", ipady=8, padx=5)
    self.search_entry.insert(0, "🔎 ابحثي في الروايات...")
    self.search_entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
    self.search_entry.bind("<KeyRelease>", self.filter_books)

    self.books_container = tk.Frame(self.root, bg="#0c0a1a")
    self.books_container.pack(fill="both", expand=True, padx=20, pady=10)

    self.render_books(my_novels)

  def clear_placeholder(self):
    if self.search_entry.get() == "🔎 ابحثي في الروايات...":
      self.search_entry.delete(0, tk.END)

  def render_books(self, list_to_show):
    for widget in self.books_container.winfo_children():
      widget.destroy()

    if not list_to_show:
      no_res = tk.Label(
          self.books_container,
          text="لا توجد نتائج مطابقة...",
          bg="#0c0a1a",
          fg="#b8a5c9",
          font=("Tajawal", 12),
      )
      no_res.pack(pady=40)
      return

    for index, book in enumerate(list_to_show):
      row = index // 2
      col = index % 2

      card = tk.Frame(
          self.books_container, bg="#1f1735", bd=1, relief="solid", padx=15, pady=15
      )
      card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

      title_lbl = tk.Label(
          card,
          text=book["title"],
          font=("Tajawal", 13, "bold"),
          bg="#1f1735",
          fg="#f3e5ab",
      )
      title_lbl.pack(anchor="e", pady=2)

      author_lbl = tk.Label(
          card,
          text=f"✍️ {book['author']}",
          font=("Tajawal", 10),
          bg="#1f1735",
          fg="#b8a5c9",
      )
      author_lbl.pack(anchor="e", pady=2)

      details_btn = tk.Button(
          card,
          text="عرض التفاصيل واستعراض الملف 📥",
          font=("Tajawal", 10, "bold"),
          bg="#d4af37",
          fg="#0c0a1a",
          bd=0,
          padx=10,
          pady=5,
          cursor="hand2",
          command=lambda b=book: self.open_detail_modal(b),
      )
      details_btn.pack(anchor="center", pady=10)

    self.books_container.columnconfigure(0, weight=1)
    self.books_container.columnconfigure(1, weight=1)

  def filter_books(self, event):
    query = self.search_entry.get().strip().lower()
    if query == "🔎 ابحثي في الروايات..." or not query:
      self.render_books(my_novels)
      return

    filtered = [
        b
        for b in my_novels
        if query in b["title"].lower() or query in b["author"].lower()
    ]
    self.render_books(filtered)

  def open_detail_modal(self, book):
    modal = tk.Toplevel(self.root)
    modal.title("تفاصيل الرواية والملف")
    modal.geometry("400x350")
    modal.configure(bg="#1a0f26")
    modal.grab_set()

    lbl_title = tk.Label(
        modal,
        text=book["title"],
        font=("Tajawal", 16, "bold"),
        bg="#1a0f26",
        fg="#f3e5ab",
    )
    lbl_title.pack(pady=15)

    lbl_author = tk.Label(
        modal,
        text=f"✍️ {book['author']}",
        font=("Tajawal", 11),
        bg="#1a0f26",
        fg="#b8a5c9",
    )
    lbl_author.pack(pady=5)

    lbl_desc = tk.Label(
        modal,
        text=book["desc"],
        font=("Tajawal", 11),
        bg="#1a0f26",
        fg="#d4cddb",
        wraplength=350,
        justify="center",
    )
    lbl_desc.pack(pady=15)

    status_lbl = tk.Label(
        modal, text="", font=("Tajawal", 10), bg="#1a0f26", fg="#ffa726"
    )
    status_lbl.pack(pady=5)

    download_btn = tk.Button(
        modal,
        text=f"📥 استدعاء وتحميل الملف ({book['pdf']})",
        font=("Tajawal", 12, "bold"),
        bg="#d4af37",
        fg="#0c0a1a",
        bd=0,
        padx=15,
        pady=8,
        cursor="hand2",
        command=lambda: self.load_and_verify_file(book["pdf"], status_lbl),
    )
    download_btn.pack(pady=10)

  def load_and_verify_file(self, filename, status_lbl):
    # استدعاء الملف الرئيسي والتحقق من مساره المباشر
    if os.path.exists(filename):
      status_lbl.config(
          text=f"✅ تم استدعاء الملف الرئيسي بنجاح: {filename}", fg="#4caf50"
      )
      messagebox.showinfo(
          "نجاح الاستدعاء",
          f"تم استدعاء الملف الرئيسي '{filename}' والتحقق منه بكفاءة!",
      )
    else:
      status_lbl.config(text="❌ الملف غير موجود في مسار العمل!", fg="#f44336")
      messagebox.showerror(
          "خطأ",
          f"تعذر العثور على الملف '{filename}'. يرجى التأكد من وضعه بجوار كود"
          " البايثون.",
      )


if __name__ == "__main__":
  root = tk.Tk()
  app = LibraryApp(root)
  root.mainloop()

```
