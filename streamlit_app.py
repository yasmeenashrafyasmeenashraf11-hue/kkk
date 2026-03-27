import streamlit as st
import google.generativeai as genai

# ===== إعداد Gemini =====
if "gemini_model" not in st.session_state:
    google_api_key = st.text_input("Google AI API Key", type="password")
    if google_api_key:
        genai.configure(api_key=google_api_key)
        st.session_state.gemini_model = genai.GenerativeModel('gemini-pro')
        st.session_state.chat = st.session_state.gemini_model.start_chat(history=[])
    else:
        st.info("الرجاء إضافة مفتاح Google AI API للمتابعة.", icon="🗝️")
        st.stop()

# ===== تهيئة الحالة =====
if "teen_data" not in st.session_state:
    st.session_state.teen_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_form" not in st.session_state:
    st.session_state.show_form = True

# ===== الواجهة الجانبية =====
with st.sidebar:
    st.title("👨‍👩‍👧‍👦 مرشد المراهقة الآمنة")

# ===== نموذج الإدخال =====
if st.session_state.show_form:
    st.title("👨‍👩‍👧‍👦 مرشد المراهقة الآمنة")

    teen_name = st.text_input("اسم المراهق")
    teen_age = st.number_input("العمر", min_value=8, max_value=25, value=15)
    teen_gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    parent_type = st.selectbox("نوع الوالد", ["الأب", "الأم", "وصي"])

    problem_description = st.text_area("وصف المشكلة")
    duration = st.selectbox("مدة المشكلة", ["أقل من أسبوع", "أكثر من شهر"])
    stress_level = st.selectbox("التوتر", ["هادئ", "متوسط", "شديد"])
    interests = st.text_input("اهتمامات المراهق")

    if st.button("ابدأ"):
        st.session_state.teen_data = {
            "name": teen_name,
            "age": teen_age,
            "gender": teen_gender,
            "parent_type": parent_type,
            "problem": problem_description,
            "duration": duration,
            "stress_level": stress_level,
            "interests": interests
        }
        st.session_state.show_form = False
        st.rerun()

# ===== الشات =====
else:
    teen = st.session_state.teen_data

    st.subheader("💬 المحادثة")

    # عرض الرسائل
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.write(f"👤: {msg['content']}")
        else:
            st.write(f"🤖: {msg['content']}")

    user_message = st.text_input("اكتب رسالتك")

    if user_message:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })

        # system prompt
        system_prompt = f"""
أنت مدرب تربية إيجابية دافئ.

المراهق:
الاسم: {teen['name']}
العمر: {teen['age']}
الجنس: {teen['gender']}

المشكلة: {teen['problem']}

التزم:
- اسأل 3 أسئلة أولاً
- أعط تحليل + خطة + سيناريو + تحذير
- كن متعاطف
"""

        try:
            response = st.session_state.chat.send_message(
                system_prompt + "\n\n" + user_message
            )

            bot_reply = response.text if hasattr(response, "text") else "صار خطأ"

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": bot_reply
            })

            st.rerun()

        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")
