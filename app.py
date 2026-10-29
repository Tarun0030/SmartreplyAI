import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Model name yahan change kar sakte ho
MODEL = "gemini-3.5-flash-lite"

st.set_page_config(
    page_title="SmartReply AI",
    page_icon="💬",
    layout="centered",
)

st.title("💬 SmartReply AI")
st.caption("Your personal AI-powered message writing assistant")

# Read the API key from .env
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "API key missing. Add GEMINI_API_KEY to your .env file "
        "and restart the app."
    )
    st.stop()

client = genai.Client(api_key=api_key)

st.subheader("Create your reply")

message = st.text_area(
    "Paste the message or describe the situation",
    placeholder=(
        "Example: A recruiter invited me for an interview "
        "tomorrow. I want to confirm politely."
    ),
    height=150,
)

col1, col2 = st.columns(2)

with col1:
    tone = st.selectbox(
        "Choose tone",
        ["Professional", "Friendly", "Formal", "Casual", "Confident"],
    )

with col2:
    language = st.selectbox(
        "Reply language",
        ["English", "Hindi", "Hinglish"],
    )

purpose = st.selectbox(
    "What do you want to do?",
    [
        "Write a new reply",
        "Improve my existing reply",
        "Make it shorter",
        "Make it more polite",
        "Reply to a recruiter",
    ],
)

existing_reply = ""

if purpose == "Improve my existing reply":
    existing_reply = st.text_area(
        "Paste your current reply",
        placeholder="Write your draft here...",
    )

if st.button("✨ Generate Reply", type="primary", use_container_width=True):
    if not message.strip():
        st.warning("Please enter a message or situation first.")

    elif purpose == "Improve my existing reply" and not existing_reply.strip():
        st.warning("Please paste your existing reply.")

    else:
        instructions = f"""
You are SmartReply AI, a helpful message-writing assistant.

Task: {purpose}
Tone: {tone}
Output language: {language}

Rules:
- Write a natural, useful, ready-to-send reply.
- Match the requested tone and language.
- Do not invent personal facts or commitments.
- Keep the reply concise unless more detail is needed.
- Return the reply only, without unnecessary explanations.
"""

        user_input = f"Message or situation:\n{message}"

        if existing_reply.strip():
            user_input += f"\n\nMy current draft:\n{existing_reply}"

        with st.spinner("Creating your reply..."):
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=user_input,
                    config=types.GenerateContentConfig(
    system_instruction=instructions,
    thinking_config=types.ThinkingConfig(thinking_level="low"),
),
                )

                answer = (response.text or "").strip()

                if answer:
                    st.session_state["last_reply"] = answer
                else:
                    st.error("The AI returned an empty response.")

            except Exception as error:
                st.error(f"Error: {error}")
                print("API error:", str(error))

if st.session_state.get("last_reply"):
    st.divider()
    st.subheader("Your generated reply")

    st.text_area(
        "Copy your reply from here",
        value=st.session_state["last_reply"],
        height=180,
        key="reply_output",
    )

    st.caption("Review the reply before sending it.")