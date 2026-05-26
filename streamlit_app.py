import streamlit as st
from google import genai

st.set_page_config(
    page_title="مرشد المراهقة الآمنة",
    page_icon="👨‍👩‍👧‍👦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

html, body, [class*="css"], .stApp, button, input, textarea, select {
    font-family: 'Cairo', sans-serif !important;
}

.main .block-container {
    direction: rtl;
    text-align: right;
    padding: 1.5rem 2rem 4rem;
    max-width: 980px;
}
section[data-testid="stSidebar"] > div {
    direction: rtl;
    text-align: right;
}

.app-header {
    background: linear-gradient(135deg, #1e3fad 0%, #4f8ef7 100%);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    box-shadow: 0 4px 24px rgba(79,142,247,0.3);
}
.app-header .icon { font-size: 3rem; }
.app-header h1 {
    margin: 0;
    font-size: 1.9rem;
    font-weight: 900;
    color: #ffffff;
}
.app-header p {
    margin: 0.3rem 0 0;
    font-size: 0.95rem;
    color: rgba(255,255,255,0.8);
}

.sec-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #4f8ef7;
    padding: 0.6rem 0;
    border-bottom: 2px solid #2a2d3e;
    margin-bottom: 1rem;
}

.chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-bottom: 1.2rem;
}
.chip {
    background: #1a1d27;
    border: 1px solid #2e3250;
    border-radius: 50px;
    padding: 0.4rem 1rem;
    font-size: 0.88rem;
    color: #c5cae9;
    font-weight: 600;
}
.chip .lbl { color: #7986cb; font-weight: 400; }

.danger-box {
    background: #2d1b1b;
    border: 1.5px solid #ef5350;
    border-radius: 12px;
    padding: 0.9rem 1.2rem;
    color: #ef9a9a;
    font-weight: 600;
    margin: 0.8rem 0;
}

.stButton > button {
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1e3fad, #4f8ef7) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 1.05rem !important;
    box-shadow: 0 4px 16px rgba(79,142,247,0.4) !important;
    width: 100% !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(79,142,247,0.55) !important;
}
.stButton > button:not([kind="primary"]) {
    background: #1a1d27 !important;
    color: #4f8ef7 !important;
    border: 2px solid #4f8ef7 !important;
}

[data-testid="stChatInput"] textarea {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
    font-size: 1rem !important;
}
[data-testid="stChatMessage"] {
    direction: rtl;
    font-family: 'Cairo', sans-serif !important;
}

.sidebar-brand {
    text-align: center;
    padding: 1rem 0 0.5rem;
}
.sidebar-brand .sb-icon { font-size: 2.8rem; }
.sidebar-brand h2 {
    font-size: 1.05rem;
    font-weight: 800;
    color: #4f8ef7;
    margin: 0.4rem 0 0;
}

.footer {
    text-align: center;
    color: #4a5068;
    font-size: 0.8rem;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #2a2d3e;
    line-height: 2;
}

label, .stSelectbox label, .stTextInput label,
.stTextArea label, .stNumberInput label {
    font-family: 'Cairo', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

if "teen_data" not in st.session_state:
    st.session_state.teen_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_form" not in st.session_state:
    st.session_state.show_form = True
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sb-icon">👨‍👩‍👧‍👦</div>
        <h2>مرشد المراهقة الآمنة</h2>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    api_input = st.text_input(
        "🔑 مفتاح Gemini API",
        type="password",
        placeholder="أدخل مفتاح API هنا",
        value=st.session_state.gemini_api_key,
        help="احصل على مفتاحك من aistudio.google.com"
    )
    if api_input:
        st.session_state.gemini_api_key = api_input

    st.divider()

    if not st.session_state.show_form and st.session_state.teen_data:
        t = st.session_state.teen_data
        st.markdown("**✅ الجلسة الحالية**")
        st.caption(f"👤 {t['name']} — {t['age']} سنة")
        st.caption(f"{'♂️' if t['gender']=='ذكر' else '♀️'} {t['gender']}  |  {t['parent_type']}")
        st.markdown("")
        if st.button("🔄 بدء جلسة جديدة", use_container_width=True):
            st.session_state.show_form = True
            st.session_state.teen_data = None
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.markdown("**📋 كيفية الاستخدام**")
        st.caption("١ — أدخل مفتاح Gemini API")
        st.caption("٢ — أدخل بيانات المراهق والمشكلة")
        st.caption("٣ — ابدأ المحادثة مع المدرب")


if st.session_state.show_form:

    st.markdown("""
    <div class="app-header">
        <div class="icon">👨‍👩‍👧‍👦</div>
        <div>
            <h1>مرشد المراهقة الآمنة</h1>
            <p>مدرب تربوي ذكي يساعدك في التعامل مع تحديات المراهقة</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">📌 بيانات المراهق</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        teen_name = st.text_input("اسم المراهق *", placeholder="أدخل الاسم")
    with c2:
        teen_age = st.number_input("العمر *", min_value=8, max_value=25, value=15)
    c1, c2 = st.columns(2)
    with c1:
        teen_gender = st.selectbox("الجنس *", ["ذكر", "أنثى"])
    with c2:
        parent_type = st.selectbox("أنت *", ["الأب", "الأم", "وصي"])

    st.markdown("")
    st.markdown('<div class="sec-title">📋 تفاصيل المشكلة</div>', unsafe_allow_html=True)
    problem_description = st.text_area(
        "وصف المشكلة *",
        placeholder="اشرح المشكلة بالتفصيل...",
        height=120
    )
    c1, c2 = st.columns(2)
    with c1:
        duration = st.selectbox("مدة المشكلة *",
            ["أقل من أسبوع", "1-2 أسبوع", "شهر واحد", "1-3 أشهر", "أكثر من 3 أشهر"])
    with c2:
        stress_level = st.selectbox("مستوى التوتر في المنزل *",
            ["الأجواء هادئة", "توتر بسيط", "توتر متوسط", "توتر شديد"])

    st.markdown("")
    st.markdown('<div class="sec-title">💡 معلومات إضافية (اختياري)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        interests = st.text_input("اهتمامات المراهق", placeholder="رياضة، موسيقى، ألعاب...")
    with c2:
        previous_attempts = st.text_input("محاولات سابقة", placeholder="ماذا جربت حتى الآن؟")

    st.markdown("<br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        go = st.button("✅ حفظ البيانات والبدء بالمحادثة", type="primary", use_container_width=True)

    if go:
        if not st.session_state.gemini_api_key.strip():
            st.error("❌ أدخل مفتاح Gemini API في الشريط الجانبي أولاً")
        elif not teen_name.strip():
            st.error("❌ أدخل اسم المراهق")
        elif not problem_description.strip():
            st.error("❌ أدخل وصف المشكلة")
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
            st.rerun()

else:
    if not st.session_state.gemini_api_key.strip():
        st.warning("⚠️ أدخل مفتاح Gemini API في الشريط الجانبي")
        st.stop()

    if not st.session_state.teen_data:
        st.warning("⚠️ لا توجد بيانات، عُد لتعبئة النموذج")
        if st.button("🔙 العودة"):
            st.session_state.show_form = True
            st.rerun()
        st.stop()

    t = st.session_state.teen_data

    st.markdown(f"""
    <div class="app-header">
        <div class="icon">💬</div>
        <div>
            <h1>جلسة مشورة — {t['name']}</h1>
            <p>تحدث مع المدرب بحرية للحصول على إرشادات مخصصة</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="chips-row">
        <div class="chip">👤 <span class="lbl">الاسم: </span>{t['name']}</div>
        <div class="chip">🎂 <span class="lbl">العمر: </span>{t['age']} سنة</div>
        <div class="chip">{'♂️' if t['gender']=='ذكر' else '♀️'} <span class="lbl">الجنس: </span>{t['gender']}</div>
        <div class="chip">🛡️ <span class="lbl">الوالد: </span>{t['parent_type']}</div>
        <div class="chip">⏱️ <span class="lbl">المدة: </span>{t['duration']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    for msg in st.session_state.chat_history:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    user_message = st.chat_input("✏️  اكتب سؤالك هنا...")

    if user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_message)

        system_prompt = f"""أنت مدرب تربية والدية محترف ومتخصص. تعمل مع {t['parent_type']}.

📌 معلومات المراهق:
- الاسم: {t['name']}
- العمر: {t['age']} سنة
- الجنس: {t['gender']}
- الاهتمامات: {t['interests']}

📋 السياق:
- المشكلة: {t['problem']}
- مدة المشكلة: {t['duration']}
- مستوى التوتر: {t['stress_level']}
- المحاولات السابقة: {t['previous_attempts']}

⚠️ تعليمات هامة:
1. لا تقدم أي تشخيصات طبية (اكتئاب، توحد، إلخ)
2. إذا شعرت أن الموقف يتطلب تدخل متخصصين، قل: "⚠️ هذا الموقف يتطلب تدخل متخصصين"
3. اقسم ردك إلى 4 أقسام بالضبط:

**1. 📌 تحليل الموقف** (فقرتان)
**2. 📋 خطة الأسبوع** (3 خطوات قابلة للقياس)
**3. 💬 سيناريو الحوار** (نص مقترح كامل)
**4. ⚠️ ما يجب تجنبه** (خطأ شائع واحد + البديل)

استجب باللغة العربية فقط، بأسلوب دافئ وتعاطفي."""

        chat_content = system_prompt + "\n\n"
        for m in st.session_state.chat_history[:-1]:
            prefix = "المستخدم" if m["role"] == "user" else "المدرب"
            chat_content += f"{prefix}: {m['content']}\n"
        chat_content += f"المستخدم: {user_message}\nالمدرب: "

        try:
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("جاري التحليل..."):
                    client = genai.Client(api_key=st.session_state.gemini_api_key)
                    response = client.models.generate_content(
                        model="models/gemini-2.5-flash",
                        contents=chat_content
                    )
                    bot_reply = response.text

                if "يتطلب تدخل متخصصين" in bot_reply or "emergency" in bot_reply.lower():
                    st.markdown('<div class="danger-box">⚠️ هذا الموقف قد يتطلب تدخل متخصصين — تواصل مع طبيب نفسي.</div>', unsafe_allow_html=True)

                st.markdown(bot_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                st.error("❌ تجاوزت الحد المسموح به. انتظر قليلاً أو استخدم مفتاح API آخر.")
            elif "401" in err or "API_KEY" in err.upper() or "INVALID" in err.upper():
                st.error("❌ مفتاح API غير صحيح.")
            else:
                st.error(f"❌ خطأ: {err}")

st.markdown("""
<div class="footer">
📧 هذا التطبيق مساعد تربوي فقط وليس بديلاً عن استشارة المتخصصين
<br>⚕️ في حالات الطوارئ تواصل مع متخصص نفسي مباشرة
</div>
""", unsafe_allow_html=True)
