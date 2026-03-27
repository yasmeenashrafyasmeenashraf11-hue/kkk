import streamlit as st
import google.generativeai as genai

# تكوين Gemini API
if "gemini_model" not in st.session_state:
    google_api_key = st.text_input("Google AI API Key", type="password")
    if google_api_key:
        # تكوين genai مع مفتاح API
        genai.configure(api_key=google_api_key)
        # إنشاء نموذج Gemini
        st.session_state.gemini_model = genai.GenerativeModel('gemini-pro')
        # إنشاء محادثة جديدة
        st.session_state.chat = st.session_state.gemini_model.start_chat()
    else:
        st.info("الرجاء إضافة مفتاح Google AI API للمتابعة.", icon="🗝️")
        st.stop()




    page_title="مرشد المراهقة الآمنة",
    page_icon="👨‍👩‍👧‍👦",
    layout="wide",
    initial_sidebar_state="expanded"


# إضافة CSS لـ RTL والألوان
st.markdown("""
    <style>
    * {
        direction: rtl;
        text-align: right;
    }
    body {
        background-color: #f5f5f5;
    }
    .stButton > button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0052a3;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    .danger-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    .info-card {
        background-color: #e7f3ff;
        border-right: 4px solid #0066cc;
        padding: 12px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .user-message {
        background-color: #0066cc;
        color: white;
        padding: 12px;
        border-radius: 5px;
        margin: 8px 0;
        text-align: right;
    }
    .bot-message {
        background-color: #e8f4f8;
        color: #333;
        padding: 12px;
        border-radius: 5px;
        margin: 8px 0;
        text-align: right;
    }
    .section-header {
        color: #0066cc;
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 2px solid #0066cc;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai

st.title("My  App")


# تهيئة session state
if "teen_data" not in st.session_state:
    st.session_state.teen_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_form" not in st.session_state:
    st.session_state.show_form = True

# ================== الواجهة الجانبية (Sidebar) ==================
with st.sidebar:
    st.image("https://img.icons8.com/color/200/000000/parenting.png", width=100)
    st.title("👨‍👩‍👧‍👦 مرشد المراهقة الآمنة ")
    st.write("---")
    
    if st.session_state.show_form:
        st.markdown("### 📋 بيانات المراهق")
    else:
        if st.session_state.teen_data:
            st.markdown("### ✅ البيانات المحفوظة")
            with st.expander("📋 عرض البيانات", expanded=False):
                st.write(f"**الاسم:** {st.session_state.teen_data['name']}")
                st.write(f"**العمر:** {st.session_state.teen_data['age']} سنة")
                st.write(f"**الجنس:** {st.session_state.teen_data['gender']}")
                st.write(f"**نوع الوالد:** {st.session_state.teen_data['parent_type']}")
                st.write("---")
                st.write(f"**المشكلة:** {st.session_state.teen_data['problem'][:100]}...")
                st.write(f"**مدة المشكلة:** {st.session_state.teen_data['duration']}")
                st.write(f"**التوتر في المنزل:** {st.session_state.teen_data['stress_level']}")
                st.write(f"**الاهتمامات:** {st.session_state.teen_data['interests']}")
            
            if st.button("🔄 تعديل البيانات"):
                st.session_state.show_form = True
                st.session_state.teen_data = None
                st.session_state.chat_history = []
                st.rerun()


# ================== الشاشة الرئيسية ==================
if st.session_state.show_form:
    # ===== قسم إدخال البيانات =====
    st.title("👨‍👩‍👧‍👦 مرشد المراهقة الآمنة")
    st.write("ملء المعلومات التالية قبل الانتقال إلى المحادثة:")
    st.write("---")
    
    # ===== القسم 1: بيانات المراهق =====
    st.markdown('<div class="section-header">📌 القسم 1: بيانات المراهق</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        teen_name = st.text_input("🔹 اسم المراهق*", placeholder="أدخل الاسم الأول")
    
    with col2:
        teen_age = st.number_input("🔹 العمر*", min_value=8, max_value=25, value=15)
    
    col1, col2 = st.columns(2)
    with col1:
        teen_gender = st.selectbox("🔹 الجنس*", ["ذكر", "أنثى"])
    
    with col2:
        parent_type = st.selectbox("🔹 نوع الوالد*", ["الأب", "الأم", "وصي"])
    
    # ===== القسم 2: تفاصيل المشكلة =====
    st.markdown('<div class="section-header">📌 القسم 2: تفاصيل المشكلة</div>', unsafe_allow_html=True)
    
    problem_description = st.text_area(
        "🔹 وصف المشكلة*",
        placeholder="اشرح المشكلة التي تواجهها مع المراهق بالتفصيل...",
        height=120
    )
    
    duration = st.selectbox(
        "🔹 مدة المشكلة*",
        ["أقل من أسبوع", "1-2 أسبوع", "شهر واحد", "1-3 أشهر", "أكثر من 3 أشهر"]
    )
    
    # ===== القسم 3: السياق والبيئة =====
    st.markdown('<div class="section-header">📌 القسم 3: السياق والبيئة</div>', unsafe_allow_html=True)
    
    stress_level = st.selectbox(
        "🔹 مستوى التوتر في المنزل*",
        ["لا، الأجواء هادئة", "نعم، توتر بسيط", "نعم، توتر متوسط", "نعم، توتر شديد جداً"]
    )
    
    previous_attempts = st.text_area(
        "🔹 المحاولات السابقة للتعامل مع المشكلة",
        placeholder="ماذا حاولت حتى الآن؟ (اختياري)",
        height=80
    )
    
    # ===== القسم 4: معلومات إضافية =====
    st.markdown('<div class="section-header">📌 القسم 4: معلومات إضافية</div>', unsafe_allow_html=True)
    
    interests = st.text_input(
        "🔹 اهتمامات المراهق",
        placeholder="مثال: الرياضة، الموسيقى، الألعاب... (اختياري)"
    )
    
    # ===== زر الحفظ =====
    st.write("---")
    
    if st.button("✅ حفظ جميع البيانات والبدء", use_container_width=True, type="primary"):
        # التحقق من البيانات المطلوبة
        if not teen_name.strip():
            st.error("❌ الرجاء إدخال اسم المراهق")
        elif not problem_description.strip():
            st.error("❌ الرجاء وصف المشكلة")
        else:
            st.session_state.teen_data = {
                "name": teen_name.strip(),
                "age": teen_age,
                "gender": teen_gender,
                "parent_type": parent_type,
                "problem": problem_description.strip(),
                "duration": duration,
                "stress_level": stress_level,
                "previous_attempts": previous_attempts.strip() or "لم يتم تحديد محاولات سابقة",
                "interests": interests.strip() or "لم يتم تحديد اهتمامات",
                
            }
            st.session_state.show_form = False
            st.session_state.chat_history = []
            st.success("✅ تم حفظ البيانات! جاهز للبدء بالمحادثة.")
            st.rerun()

else:
    # ===== منطقة المحادثة =====
    if st.session_state.teen_data:
        # عرض بطاقة المعلومات
        teen = st.session_state.teen_data
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="info-card">
            <strong>👤 الاسم</strong><br>
            {teen['name']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-card">
            <strong>🎂 العمر</strong><br>
            {teen['age']} سنة
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="info-card">
            <strong>👥 الجنس</strong><br>
            {teen['gender']}
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="info-card">
            <strong>🛡️ نوع الوالد</strong><br>
            {teen['parent_type']}
            </div>
            """, unsafe_allow_html=True)
        
        st.write("---")
        
        # منطقة السجل
        st.subheader("💬 حوار المشورة الوالدية")
        
        # عرض السجل
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f'<div class="user-message">👤 أنت:<br>{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-message">🤖 المدرب:<br>{message["content"]}</div>', unsafe_allow_html=True)
        
        st.write("---")
        
        # إدخال الرسالة
        user_message = st.text_input("📝 اكتب رسالتك هنا...", placeholder="اسأل المدرب أي شيء...")
        
        if user_message:
            # إضافة الرسالة للسجل
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_message
            })
            
            # بناء System Prompt
            system_prompt = f"""أنت مدرب تربية والدية محترف ومتخصص. تعمل مع {teen['parent_type']}.

📌 معلومات المراهق:
- الاسم: {teen['name']}
- العمر: {teen['age']} سنة
- الجنس: {teen['gender']}
- الاهتمامات: {teen['interests']}

📋 السياق:
- المشكلة: {teen['problem']}
- مدة المشكلة: {teen['duration']}
- مستوى التوتر: {teen['stress_level']}
- المحاولات السابقة: {teen['previous_attempts']}

⚠️ تعليمات هامة:
1. لا تقدم أي تشخيصات طبية (اكتئاب، توحد، إلخ)
2. إذا شعرت أن الموقف يتطلب تدخل متخصصين، قل: "⚠️ هذا الموقف يتطلب تدخل متخصصين - الرجاء التواصل مع مختص نفسي"
3. اقسم ردك إلى 4 أقسام بالضبط:

**1. 📌 تحليل الموقف** (فقرتان):
- شرح السلوك بعمق
- ربط بحاجات النمو في سن المراهقة

**2. 📋 خطة الأسبوع** (3 خطوات بالضبط):
- صيغة: "الخطوة X: [افعل Y بحيث Z]"
- قابلة للقياس

**3. 💬 سيناريو الحوار**:
- نص مقترح كامل بين علامتي تنصيص
- يمكن قراءته مباشرة مع المراهق

**4. ⚠️ ما يجب تجنبه** (خطأ واحد شائع):
- توضيح الخطأ الشائع
- السبب
- البديل الصحيح

استجب باللغة العربية فقط، بأسلوب دافئ وتعاطفي."""
            
            # استدعاء OpenAI API
            try:
                with st.spinner("🤖 المدرب يفكر..."):
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *st.session_state.chat_history
                        ],
                        temperature=0.7,
                        max_tokens=1500
                    )
                    
                    bot_reply = response.choices[0].message.content
                    
                    # التحقق من التحذيرات الأمنية
                    if "يتطلب تدخل متخصصين" in bot_reply or "emergency" in bot_reply.lower():
                        st.markdown("""
                        <div class="danger-message">
                        ⚠️ <strong>تنبيه هام:</strong> هذا الموقف قد يتطلب تدخل متخصصين. 
                        الرجاء التواصل مع طبيب نفسي أو متخصص في علم نفس المراهقين.
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": bot_reply
                    })
                    
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ حدث خطأ: {str(e)}")
                st.session_state.chat_history.pop()  # إزالة الرسالة في حالة الخطأ


# Footer
st.write("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 12px;">
📧 هذا التطبيق مصمم لتقديم مشورة والدية مساعدة فقط، وليس بديلاً عن استشارة المتخصصين.<br>
⚕️ في حالات الطوارئ، الرجاء التواصل مع متخصص نفسي مباشرة.
</div>
""", unsafe_allow_html=True)

