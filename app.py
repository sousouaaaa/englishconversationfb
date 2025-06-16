import openai
import streamlit as st

# OpenAI APIキーをsecretsから取得（Streamlit Cloud用）
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="英会話フィードバック", layout="centered")
st.title("\U0001F4AC 英会話フィードバックアプリ")

st.markdown("""
#### 録音した英会話音声をアップロードすると、文字起こしとAIによるフィードバックが得られます。
""")

audio_file = st.file_uploader("\U0001F3A4 録音ファイルをアップロード（mp3, wav, m4a）", type=["mp3", "wav", "m4a"])

if audio_file:
    with st.spinner("\u6587\u5b57\u8d77\u3053\u3057\u4e2d..."):
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    st.subheader("\u6587\u5b57\u8d77\u3053\u3057\u7d50\u679c")
    st.write(transcript["text"])

    with st.spinner("\u30d5\u30a3\u30fc\u30c9\u30d0\u30c3\u30af\u751f\u6210\u4e2d..."):
        prompt = f"""
あなたは英会話の専門コーチです。
以下の英会話文を読み、以下の観点でフィードバックしてください：
1. 総合点（100点満点）
2. 文法や表現のミス
3. 改善提案
4. 学習アドバイス

【会話文】
{transcript["text"]}
"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

    st.subheader("\U0001F4DD フィードバック")
    st.write(response["choices"][0]["message"]["content"])