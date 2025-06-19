import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="英会話フィードバック", layout="centered")
st.title("💬 英会話フィードバックアプリ")
st.markdown("#### 録音した英会話音声をアップロードすると、文字起こしとAIによるフィードバックが得られます。")

audio_file = st.file_uploader("🎤 録音ファイルをアップロード（mp3, wav, m4a）", type=["mp3", "wav", "m4a"])

if audio_file:
    with st.spinner("文字起こし中..."):
        # 正しい書き方（現APIに対応）
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    st.subheader("📄 文字起こし結果")
    st.write(transcript.text)

    with st.spinner("フィードバック生成中..."):
        prompt = f"""
あなたは英会話の専門コーチです。
以下の英会話文を読み、以下の観点でフィードバックしてください：
1. 総合点（100点満点）
2. 文法や表現のミス
3. 改善提案
4. 学習アドバイス

【会話文】
{transcript.text}
"""
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

    st.subheader("📝 フィードバック")
    st.write(response.choices[0].message.content)
