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
        * { box-sizing: border-box; font-family: 'Arial', sans-serif; }
        body { background-color: #fafafa; min-height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center; color: #333; }
        .container { width: 90%; max-width: 700px; text-align: center; padding: 20px; }
        
        h1 { font-size: 32px; font-weight: bold; color: #111; margin-bottom: 40px; }
        
        .enter-btn { background-color: #111; color: white; padding: 14px 50px; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; transition: 0.2s; font-weight: bold; }
        .enter-btn:hover { background-color: #333; }
        
        #books-section { display: none; margin-top: 20px; text-align: right; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 10px; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
        th, td { padding: 16px; text-align: center; border-bottom: 1px solid #eee; font-size: 15px; }
        th { background-color: #f5f5f5; color: #666; font-weight: bold; }
        
        .status { font-size: 14px; font-weight: bold; }
        .status-available { color: #2e7d32; }
        .status-borrowed { color: #c62828; }
        
        .view-pdf-btn { color: #0066cc; text-decoration: none; font-size: 15px; font-weight: bold; }
        .view-pdf-btn:hover { text-decoration: underline; }
    </style>
    <script>
        function showBooks() {
            document.getElementById("login-panel").style.display = "none";
            document.getElementById("books-section").style.display = "block";
        }
    </script>
</head>
<body>
    <div class="container">
        <div id="login-panel">
            <h1>مكتبتي 📚</h1>
            <br>
            <button class="enter-btn" onclick="showBooks()">دخول</button>
        </div>
        
        <div id="books-section">
            <h2 style="font-size: 24px; font-weight: bold; margin-bottom: 20px; text-align: center; color: #111;">الكتب المتاحة</h2>
            <table>
                <thead>
                    <tr>
                        <th>الرقم</th>
                        <th>عنوان الكتاب</th>
                        <th>المؤلف</th>
                        <th>الحالة</th>
                        <th>الملف</th>
                    </tr>
                </thead>
                <tbody>
                    {% for book in books %}
                    <tr>
                        <td>{{ book.id }}</td>
                        <td style="color: #111; font-weight: 600;">{{ book.title }}</td>
                        <td>{{ book.author }}</td>
                        <td>
                            <span class="{% if book.status == 'متاح' %}status-available{% else %}status-borrowed{% endif %}">
                                {{ book.status }}
                            </span>
                        </td>
                        <td>
                            <a href="{{ book.pdf_url }}" target="_blank" class="view-pdf-btn">عرض PDF</a>
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
