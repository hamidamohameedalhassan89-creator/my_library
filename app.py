from flask import Flask, render_template_string, request, redirect, url_for
import os

app = Flask(__name__)

# قاعدة بيانات الكتب مع روابط ملفات PDF حقيقية ومباشرة للتشغيل سحابياً
books_db = [
    {
        "id": 1, 
        "title": "مقدمة في الحوسبة السحابية", 
        "author": "د. أحمد علي", 
        "status": "متاح",
        "pdf_url": "https://www.ece.rutgers.edu/~pompili/ECE568/Cloud_Computing_Introduction.pdf"
    },
    {
        "id": 2, 
        "title": "برمجة الحاويات باستخدام Docker", 
        "author": "مهندس خالد محمد", 
        "status": "مستعار",
        "pdf_url": "https://dockerlabs.collabnix.com/docker-cheatsheet.pdf"
    },
    {
        "id": 3, 
        "title": "أمن المعلومات والتشفير", 
        "author": "د. سارة عمر", 
        "status": "متاح",
        "pdf_url": "https://cs.stanford.edu/people/eroberts/courses/cs181/projects/cryptography/cryptography.pdf"
    }
]

# تصميم صفحة الدخول
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول | المكتبة الرقمية</title>
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100vh; display: flex; justify-content: center; align-items: center; margin: 0; }
        .login-card { background: white; padding: 45px 35px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; text-align: center; }
        h2 { color: #2d3748; margin-bottom: 10px; font-size: 24px; }
        p { color: #718096; font-size: 14px; margin-bottom: 30px; }
        .input-group { margin-bottom: 20px; text-align: right; }
        label { display: block; color: #4a5568; margin-bottom: 5px; font-size: 14px; font-weight: 600; }
        input { width: 100%; padding: 12px 15px; border: 2px solid #e2e8f0; border-radius: 10px; outline: none; transition: 0.3s; font-size: 15px; }
        input:focus { border-color: #667eea; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; width: 100%; padding: 12px; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.3s; box-shadow: 0 4px 6px rgba(50,50,93,0.11); }
        .btn:hover { opacity: 0.9; transform: translateY(-1px); }
        .error { color: #e53e3e; font-size: 14px; margin-bottom: 15px; text-align: right; }
    </style>
</head>
<body>
    <div class="login-card">
        <h2>مرحباً بكِ 🔐</h2>
        <p>سجلي الدخول للوصول إلى نظام المكتبة السحابي</p>
        
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        
        <form method="POST">
            <div class="input-group">
                <label>اسم المستخدم</label>
                <input type="text" name="username" placeholder="ادخلي اسم المستخدم" required>
            </div>
            <div class="input-group">
                <label>كلمة المرور</label>
                <input type="password" name="password" placeholder="ادخلي كلمة المرور" required>
            </div>
            <button type="submit" class="btn">دخول للنظام 🚀</button>
        </form>
    </div>
</body>
</html>
"""

# تصميم لوحة التحكم الفخمة مع أزرار استعراض الكتب الـ PDF واختيار العرض
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم | المكتبة الرقمية</title>
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #f7fafc; margin: 0; padding: 20px; }
        .dashboard { max-width: 900px; margin: 30px auto; background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #edf2f7; padding-bottom: 20px; margin-bottom: 30px; }
        h1 { color: #2d3748; font-size: 24px; margin: 0; }
        .logout-btn { background-color: #e53e3e; color: white; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: bold; }
        
        .main-action { text-align: center; margin-bottom: 30px; background: #f0f4ff; padding: 20px; border-radius: 12px; border: 1px dashed #667eea; }
        .show-books-btn { background: #4c51bf; color: white; padding: 12px 25px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .show-books-btn:hover { background: #434190; }
        
        #books-section { display: none; transition: 0.5s ease-in-out; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 15px; text-align: center; border-bottom: 1px solid #e2e8f0; }
        th { background-color: #4a5568; color: white; font-weight: 600; }
        tr:hover { background-color: #f8fafc; }
        
        .status { padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .status-available { background-color: #c6f6d5; color: #22543d; }
        .status-borrowed { background-color: #fed7d7; color: #742a2a; }
        
        .view-pdf-btn { background-color: #319795; color: white; padding: 6px 14px; border: none; border-radius: 6px; font-size: 13px; font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; transition: 0.2s; }
        .view-pdf-btn:hover { background-color: #2c7a7b; }
    </style>
    <script>
        function toggleBooks() {
            var section = document.getElementById("books-section");
            if (section.style.display === "none" || section.style.display === "") {
                section.style.display = "block";
                document.getElementById("action-text").innerText = "لوحة إدارة الكتب الحالية المتوفرة بسيرفر السحابة:";
            } else {
                section.style.display = "none";
                document.getElementById("action-text").innerText = "اضغطي على الزر بالأسفل لاستعراض الكتب الرقمية المخزنة سحابياً";
            }
        }
    </script>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>نظام إدارة المكتبة الرقمية السحابية 📊</h1>
            <a href="/" class="logout-btn">تسجيل الخروج ↩️</a>
        </div>
        
        <div class="main-action">
            <h3 id="action-text" style="color: #4a5568; margin-top: 0;">اضغطي على الزر بالأسفل لاستعراض الكتب الرقمية المخزنة سحابياً</h3>
            <button class="show-books-btn" onclick="toggleBooks()">عرض الكتب المتاحة 📚</button>
        </div>
        
        <div id="books-section">
            <table>
                <thead>
                    <tr>
                        <th>الرقم التسلسلي</th>
                        <th>عنوان الكتاب</th>
                        <th>المؤلف / المشرف</th>
                        <th>حالة الكتاب</th>
                        <th>الملف الرقمي (PDF)</th>
                    </tr>
                </thead>
                <tbody>
                    {% for book in books %}
                    <tr>
                        <td>#{{ book.id }}</td>
                        <td style="font-weight: 600; color: #2d3748;">{{ book.title }}</td>
                        <td>{{ book.author }}</td>
                        <td>
                            <span class="status {% if book.status == 'متاح' %}status-available{% else %}status-borrowed{% endif %}">
                                {{ book.status }}
                            </span>
                        </td>
                        <td>
                            <a href="{{ book.pdf_url }}" target="_blank" class="view-pdf-btn">قراءة وتحميل PDF 📄</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # بيانات الدخول التجريبية الخاصة بكِ وللدكتورة
        if request.form['username'] == 'admin' and request.form['password'] == '1234':
            return render_template_string(DASHBOARD_TEMPLATE, books=books_db)
        else:
            error = 'اسم المستخدم أو كلمة المرور غير صحيحة! ❌'
    return render_template_string(LOGIN_TEMPLATE, error=error)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
