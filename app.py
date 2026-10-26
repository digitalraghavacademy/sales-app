import streamlit as st
import pandas as pd

st.title("दुकान की बिक्री रिपोर्ट")

uploaded = st.file_uploader("अपनी CSV file चुनें", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    # File न होने पर demo data दिखेगा
    df = pd.DataFrame({
        "date": ["2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05"],
        "item": ["चाय", "बिस्कुट", "चाय", "समोसा", "बिस्कुट"],
        "sales": [500, 300, 700, 450, 280],
    })
    st.info("अभी demo data दिख रहा है। अपनी file डालने पर आपका data दिखेगा।")

st.subheader("आपका डेटा")
st.dataframe(df)

st.subheader("मुख्य नतीजे")
st.metric("कुल बिक्री (₹)", int(df["sales"].sum()))
st.metric("औसत बिक्री (₹)", round(df["sales"].mean(), 2))

st.subheader("सामान के हिसाब से बिक्री")
st.bar_chart(df.groupby("item")["sales"].sum())