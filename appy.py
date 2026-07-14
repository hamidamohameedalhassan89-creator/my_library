import streamlit as st
import os

# 1. إعدادات الصفحة الأساسية بشكل عصري
st.set_page_config(
    page_title="المكتبة الرقمية السحابية", 
    page_icon="📚", 
    layout="wide"
)

# 2. تصميم عصري وجميل (CSS) مخصص للهواتف والشاشات المتجاوبة
st.markdown("""
    <style>
    /* تنسيق النص للغة العربية */
    .main { text-align: right; direction: rtl; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* تصميم كروت الكتب بشكل احترافي */
    .book-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-right: 5px solid #4CAF50;
    }
    
    /* تنسيق أزرار التحميل لتكون جذابة وعصرية */
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

# واجهة التطبيق الترحيبية
st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("📚 مكتبة الروايات والكتب الرقمية السحابية")
st.subheader("منصة ذكية ومطورة لعرض وتحميل الكتب مباشرة عبر السحابة ☁️")
st.write("---")

# 3. قاعدة البيانات مع التأكيد الحاسم على الامتدادات الصحيحة لملفاتكِ
novels = [
    {
        "title": "كتاب الأمير",
        "author": "نيقولا ميكافيلي",
        "genre": "كتب سياسية وفلسفية",
        "description": "دراسة في الفقه السياسي أعدها ميكافيلي في القرن السادس عشر كدليل عملي للحكام.",
        "cover_path": "أمير.png",
        "pdf_path": "أمير.pdf"
    },
    {
        "title": "رواية أماريتا",
        "author": "عمرو عبد الحميد",
        "genre": "روايات خيال وفانتازيا",
        "description": "الجزء الثاني من رواية أرض زيكولا، تأخذنا في رحلة مشوقة لقوانين تحكم هذا العالم الخيالي.",
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
