import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8000))

html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>المكتبة المتكاملة 📚</title>
    <style>
        @import url('[https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap](https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap)');
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Tajawal', sans-serif; }
        body {
            min-height: 100vh;
            background: linear-gradient(145deg, #0c0a1a 0%, #1f1735 40%, #2a1f42 100%);
            color: #f0e6f5;
            padding: 20px;
        }
        .container { max-width: 1300px; margin: 0 auto; }
        .screen { display: none; }
        .screen.active-screen { display: block; }
        .welcome-screen { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 85vh; text-align: center; }
        .welcome-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 40px;
            padding: 50px 30px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        }
        .welcome-card h1 {
            font-size: 36px; font-weight: 800;
            background: linear-gradient(135deg, #f3e5ab, #d4af37);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
        }
        .welcome-card p { font-size: 18px; color: #b8a5c9; margin-bottom: 35px; }
        .enter-btn {
            background: linear-gradient(135deg, #d4af37, #b8962e);
            border: none; color: #0c0a1a;
            padding: 16px 40px; border-radius: 60px;
            font-size: 20px; font-weight: 800; cursor: pointer;
            box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3);
        }
        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 18px 30px; background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 60px;
            margin-bottom: 25px;
        }
        .header h1 {
            font-size: 26px; font-weight: 800;
            background: linear-gradient(135deg, #f3e5ab, #d4af37);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .back-nav-btn {
            background: transparent; border: 1px solid #d4af37; color: #d4af37;
            padding: 6px 16px; border-radius: 30px; cursor: pointer; font-weight: 700;
            margin-bottom: 15px;
        }
        .greeting { font-size: 24px; font-weight: 700; margin-bottom: 15px; color: #f3e5ab; }
        .books-grid {
            display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 25px;
        }
        .book-card {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 24px; overflow: hidden; cursor: pointer; transition: 0.3s;
        }
        .book-card:hover { transform: translateY(-8px); border-color: rgba(212, 175, 55, 0.4); }
        .book-cover { width: 100%; aspect-ratio: 2/3; object-fit: cover; background: #2a1f42; }
        .book-info { padding: 14px 16px; }
        .book-title { font-weight: 800; font-size: 17px; color: #f3e5ab; }
        .book-author { font-size: 14px; color: #b8a5c9; margin-top: 4px; }
        .modal-overlay {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.7); justify-content: center; align-items: center; z-index: 999;
        }
        .modal-overlay.open { display: flex; }
        .modal-card {
            background: #1a0f26; border: 1px solid rgba(212, 175, 55, 0.25);
            border-radius: 40px; max-width: 450px; width: 100%; padding: 30px; text-align: center; position: relative;
        }
        .modal-close { position: absolute; top: 15px; left: 20px; background: none; border: none; font-size: 26px; color: #d4af37; cursor: pointer; }
        .detail-cover { width: 140px; height: 200px; object-fit: cover; border-radius: 16px; margin-bottom: 15px; }
        .download-btn {
            background: linear-gradient(135deg, #d4af37, #b8962e); border: none; color: #0c0a1a;
            padding: 14px; border-radius: 50px; font-size: 18px; font-weight: 800; cursor: pointer; width: 100%; margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="screen1" class="screen active-screen welcome-screen">
            <div class="welcome-card">
                <h1>📚 مكتبة الروايات الخاصة</h1>
                <p>مرحباً بكِ يا حميدة في مكتبتك الرقمية المميزة.</p>
                <button class="enter-btn" onclick="goToScreen2()">دخول المكتبة 📖</button>
            </div>
        </div>
        <div id="screen2" class="screen">
            <button class="back-nav-btn" onclick="goToScreen1()">⬅ العودة للرئيسية</button>
            <header class="header">
                <h1>✨ روايات حميدة المميزة</h1>
            </header>
            <div class="greeting">مرحباً بكِ مجدداً 🌸</div>
            <div class="books-grid" id="booksGrid"></div>
        </div>
    </div>
    <div class="modal-overlay" id="detailModal">
        <div class="modal-card">
            <button class="modal-close" onclick="closeDetail()">✕</button>
            <img class="detail-cover" id="detailCover" src="" alt="غلاف" />
            <div id="detailTitle" style="font-size:22px; font-weight:800; color:#f3e5ab;"></div>
            <div id="detailAuthor" style="font-size:15px; color:#b8a5c9; margin-bottom:15px;"></div>
            <button class="download-btn" onclick="downloadCurrentBook()">📥 تحميل الملف (PDF)</button>
            <div id="downloadStatus" style="margin-top:10px; font-size:14px;"></div>
        </div>
    </div>
    <script>
        const myNovels = [
            { id: 1, title: 'ملف الأمير التوثيقي', author: 'Ameer Document', cover: 'facer.png', pdf: 'ameer.pdf' },
            { id: 2, title: 'مملكة الفعاليات والأنظمة', author: 'Almamlaka System', cover: 'mamlaka.png', pdf: 'mamlaka.pdf' },
            { id: 3, title: 'أرض الذكاء الاصطناعي والحوسبة', author: 'Ardzekola AI', cover: 'ardzekola.png', pdf: 'ardzekola.pdf' },
            { id: 4, title: 'وادي التقنية والحلول البرمجية', author: 'Wady Technology', cover: 'wady.png', pdf: 'wady.pdf' }
        ];
        let selectedNovel = null;
        function goToScreen2() {
            document.getElementById('screen1').classList.remove('active-screen');
            document.getElementById('screen2').classList.add('active-screen');
            renderBooks();
        }
        function goToScreen1() {
            document.getElementById('screen2').classList.remove('active-screen');
            document.getElementById('screen1').classList.add('active-screen');
        }
        function renderBooks() {
            const grid = document.getElementById('booksGrid');
            grid.innerHTML = '';
            myNovels.forEach(book => {
                const card = document.createElement('div');
                card.className = 'book-card';
                card.innerHTML = `<img class="book-cover" src="${book.cover}" /><div class="book-info"><div class="book-title">${book.title}</div><div class="book-author">✍️ ${book.author}</div></div>`;
                card.onclick = () => openDetail(book);
                grid.appendChild(card);
            });
        }
        function openDetail(book) {
            selectedNovel = book;
            document.getElementById('detailCover').src = book.cover;
            document.getElementById('detailTitle').textContent = book.title;
            document.getElementById('detailAuthor').textContent = '✍️ ' + book.author;
            document.getElementById('downloadStatus').textContent = '';
            document.getElementById('detailModal').classList.add('open');
        }
        function closeDetail() { document.getElementById('detailModal').classList.remove('open'); }
        function downloadCurrentBook() {
            if (!selectedNovel) return;
            window.location.href = selectedNovel.pdf;
        }
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()
