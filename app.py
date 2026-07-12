from flask import Flask, render_template_string, os

app = Flask(__name__)

# قاعدة بيانات الكتب
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

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مكتبتي</title>
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; }
        .wrapper { width: 100%; max-width: 850px; background: white; padding: 40px; border-radius: 24px; box-shadow: 0 15px 35px rgba(0,0,0,0.08); text-align: center; }
        
        h1 { color: #2d3748; font-size: 32px; margin: 0 0 10px 0; font-weight: 700; letter-spacing: -0.5px; }
        .divider { width: 60px; height: 4px; background: #667eea; margin: 0 auto 30px auto; border-radius: 2px; }
        
        .login-section { padding: 20px 0; }
        .enter-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 14px 45px; border: none; border-radius: 12px; font-size: 18px; font-weight: bold; cursor: pointer; transition: 0.3s; box-shadow: 0 5px 15px rgba(102,126,234,0.4); }
        .enter-btn:hover { opacity: 0.95; transform: translateY(-2px); }
        
        #books-section { display: none; margin-top: 20px; animation: fadeIn 0.6s ease-in-out forwards; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
        th, td { padding: 16px; text-align: center; border-bottom: 1px solid #edf2f7; }
        th { background-color: #4a5568; color: white; font-weight: 600; font-size: 15px; }
        tr:hover { background-color: #f8fafc; }
        
        .status { padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .status-available { background-color: #c6f6d5; color: #22543d; }
        .status-borrowed { background-color: #fed7d7; color: #742a2a; }
        
        .view-pdf-btn { background-color: #319795; color: white; padding: 8px 18px; border: none; border-radius: 8px; font-size: 13px; font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; transition: 0.2s; box-shadow: 0 4px 6px rgba(49,151,149,0.15); }
        .view-pdf-btn:hover { background-color: #2c7a7b; transform: translateY(-1px); }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    <script>
        function showBooks() {
            document.getElementById("login-panel").style.display = "none";
            document.getElementById("books-section").style.display = "block";
        }
    </script>
</head>
<body>
    <div class="wrapper">
        <h1>مكتبتي 📚</h1>
        <div class="divider"></div>
        
        <div id="login-panel" class="login-section">
            <button class="enter-btn" onclick="showBooks()">دخول 🚀</button>
        </div>
        
        <div id="books-section">
            <table>
                <thead>
                    <tr>
                        <th>الرقم</th>
                        <th>عنوان الكتاب</th>
                        <th>المؤلف</th>
                        <th>الحالة</th>
                        <th>الملف الرقمي</th>
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
                            <a href="{{ book.pdf_url }}" target="_blank" class="view-pdf-btn">عرض الكتاب 📄</a>
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

@app.route('/')
def index():
    return render_template_string(MAIN_TEMPLATE, books=books_db)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
