from flask import Flask, render_template_string
import os

app = Flask(__name__)

# قاعدة بيانات تجريبية داخل التطبيق لإدارة الكتب
books_db = [
    {"id": 1, "title": "مقدمة في الحوسبة السحابية", "author": "د. أحمد علي", "status": "متاح"},
    {"id": 2, "title": "برمجة الحاويات باستخدام Docker", "author": "مهندس خالد محمد", "status": "مستعار"},
    {"id": 3, "title": "أمن المعلومات والتشفير", "author": "د. سارة عمر", "status": "متاح"}
]

# واجهة مستخدم تفاعلية للتطبيق السحابي
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تطبيق المكتبة الرقمية السحابي</title>
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #f4f6f9; margin: 0; padding: 15px; text-align: center; }
        .container { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; font-size: 20px; }
        p { color: #7f8c8d; font-size: 14px; }
        .btn { background-color: #2980b9; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 15px; margin-bottom: 15px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        th { background-color: #2c3e50; color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .status-available { color: green; font-weight: bold; }
        .status-borrowed { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>تطبيق إدارة المكتبة الرقمية السحابي 🚀</h1>
        <p>تطبيق Python تفاعلي يعمل داخل حاوية معزولة على السحابة</p>
        
        <button class="btn" onclick="location.reload()">تحديث البيانات 🔄</button>
        
        <table>
            <thead>
                <tr>
                    <th>الرقم</th>
                    <th>عنوان الكتاب</th>
                    <th>المؤلف</th>
                    <th>الحالة</th>
                </tr>
            </thead>
            <tbody>
                {% for book in books %}
                <tr>
                    <td>{{ book.id }}</td>
                    <td>{{ book.title }}</td>
                    <td>{{ book.author }}</td>
                    <td>
                        <span class="{% if book.status == 'متاح' %}status-available{% else %}status-borrowed{% endif %}">
                            {{ book.status }}
                        </span>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, books=books_db)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
