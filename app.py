import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Raghav Book Academy", page_icon="🛒", layout="wide")

st.title("Raghav Book Academy - किराना बिक्री रिपोर्ट")

uploaded = st.file_uploader("अपनी CSV file चुनें", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    df = pd.DataFrame({
        "date": ["2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05"],
        "item": ["चाय", "बिस्कुट", "चाय", "समोसा", "बिस्कुट"],
        "sales": [500, 300, 700, 450, 280],
    })
    st.info("अभी demo data दिख रहा है। अपनी CSV file डालने पर आपका data दिखेगा।")

st.subheader("आपका डेटा")
st.dataframe(df)

# मुख्य नतीजे
item_sales = df.groupby("item")["sales"].sum().reset_index()
avg_sales = item_sales["sales"].mean()
top_item = item_sales.sort_values("sales", ascending=False).iloc[0]

st.subheader("मुख्य नतीजे")
col1, col2, col3 = st.columns(3)
col1.metric("कुल बिक्री (₹)", int(df["sales"].sum()))
col2.metric("औसत बिक्री (₹)", round(df["sales"].mean(), 2))
col3.metric("सबसे ज़्यादा बिकने वाला", top_item["item"])

# रोज़ की बिक्री
st.subheader("रोज़ की बिक्री")
daily = df.groupby("date")["sales"].sum().reset_index()
daily_chart = alt.Chart(daily).mark_bar(color="#1E88E5").encode(
    x=alt.X("date", title="तारीख"),
    y=alt.Y("sales", title="बिक्री (₹)"),
    tooltip=["date", "sales"],
).properties(height=300)
st.altair_chart(daily_chart, use_container_width=True)

# सामान के हिसाब से chart: ज़्यादा बिकने वाला हरा, कम बिकने वाला लाल
st.subheader("सामान के हिसाब से बिक्री")
item_sales["status"] = item_sales["sales"].apply(
    lambda s: "ज़्यादा बिक्री" if s >= avg_sales else "कम बिक्री"
)
item_chart = alt.Chart(item_sales).mark_bar().encode(
    x=alt.X("item", sort="-y", title="सामान"),
    y=alt.Y("sales", title="बिक्री (₹)"),
    color=alt.Color(
        "status",
        scale=alt.Scale(domain=["ज़्यादा बिक्री", "कम बिक्री"], range=["#2E7D32", "#E53935"]),
        legend=alt.Legend(title="स्थिति"),
    ),
    tooltip=["item", "sales"],
).properties(height=350)
st.altair_chart(item_chart, use_container_width=True)

st.caption("हरा रंग = ज़्यादा बिकने वाला सामान, लाल रंग = कम बिकने वाला सामान")