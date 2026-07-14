import streamlit as st
import os

# 1. إعدادات الصفحة الأساسية بشكل عصري
st.set_page_config(
    page_title="المكتبة الرقمية", 
    page_icon="📚", 
    layout="wide"
)

# 2. تصميم عصري وجميل (CSS) مخصص للهواتف والشاشات المتجاوبة
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .book-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-right: 5px solid #4CAF50;
    }
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        border-radius: 8px;
        padding: 10px;
        font-weight: bold;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# واجهة التطبيق الترحيبية المعدلة حسب طلبكِ
st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("📚 مكتبة الروايات والكتب الرقمية")
st.subheader("منصة ذكية لعرض وتحميل الكتب... مرحبا بكم")
st.write("---")

# 3. قاعدة البيانات مع الأسماء الإنجليزية الصحيحة لكتاب الأمير
novels = [
    {
        "title": "كتاب الأمير",
        "author": "نيقولا ميكافيلي",
        "genre": "كتب سياسية وفلسفية",
        "description": "دراسة في الفقه السياسي أعدها ميكافيلي في القرن السادس عشر كدليل عملي للحكام.",
        "cover_path": "ameer.png",
        "pdf_path": "ameer.pdf"
    },
    {
        "title": "رواية أماريتا",
        "author": "عمرو عبد الحميد",
        "genre": "روايات خيال وفانتازيا",
        "description": "الجزء الثاني من رواية أرض زيكولا، تأخذنا في رحلة مشوقة لقوانين تحكم هذا عالم الخيالي.",
        "cover_path": "ardzekola.png",
        "pdf_path": "ardzekola.pdf"
    },
    {
        "title": "فكر كأنك طبيب نفسي",
        "author": "د. أسامة الشبيلي",
        "genre": "تطوير ذات وعلم نفس",
        "description": "كتاب رائع يساعدك على فهم طرائق التفكير وتحليل السلوكيات وتطوير أدوات التعامل مع الذات.",
        "cover_path": "facer.png",
        "pdf_path": "facer.pdf"
    },
    {
        "title": "وادي الذئاب المنسية",
        "author": "عماد البليك",
        "genre": "روايات الغموض والإثارة",
        "description": "رواية مليئة بالغموض تأخذ القارئ في دروب شائكة ومغامرة مشوقة لحل الأسرار المنسية.",
        "cover_path": "wady.png",
        "pdf_path": "wady.pdf"
    },
    {
        "title": "رواية مملكة",
        "author": "حنان لاشين",
        "genre": "روايات خيال وفانتازيا",
        "description": "رواية مشوقة تأخذ القارئ في رحلة داخل عوالم غامضة وصراعات مثيرة في مملكة منسية.",
        "cover_path": "mamlaka.png",
        "pdf_path": "mamlaka.pdf"
    }
]

# 4. الشريط الجانبي
st.sidebar.header("🔍 تصفية وبحث")
selected_genre = st.sidebar.selectbox("اختر تصنيف الكتب:", [
    "الكل", 
    "كتب سياسية وفلسفية", 
    "روايات خيال وفانتازيا", 
    "تطوير ذات وعلم نفس", 
    "روايات الغموض والإثارة"
])

st.sidebar.write("---")
st.sidebar.markdown("""
### 👥 فريق عمل المشروع:
* **قائدة المشروع:** [اسمكِ هنا]
* **إعداد وتنسيق وميديا:** آمال وبقية الفريق
""")

# تصفية الكتب بناءً على الاختيار
filtered_novels = novels if selected_genre == "الكل" else [n for n in novels if n["genre"] == selected_genre]

st.write(f"### الكتب المتاحة حالياً ({len(filtered_novels)}):")

# 5. عرض الكتب في أعمدة متناسقة
cols = st.columns(len(filtered_novels) if len(filtered_novels) > 0 else 1)

for i, novel in enumerate(filtered_novels):
    with cols[i]:
        if os.path.exists(novel["cover_path"]):
            st.image(novel["cover_path"], use_container_width=True)
        else:
            st.image("https://via.placeholder.com/180x250?text=📚", use_container_width=True)
            
        st.markdown(f"### {novel['title']}")
        st.caption(f"✍️ {novel['author']} | 🏷️ {novel['genre']}")
        st.write(novel["description"])
        
        if os.path.exists(novel["pdf_path"]):
            with open(novel["pdf_path"], "rb") as pdf_file:
                pdf_data = pdf_file.read()
            st.download_button(
                label="📥 تحميل PDF",
                data=pdf_data,
                file_name=novel["pdf_path"],
                mime="application/pdf",
                key=f"dl_{i}"
            )
        else:
            st.error("⚠️ ملف الكتاب غير متوفر.")
        st.write("---")

st.markdown('</div>', unsafe_allow_html=True)
