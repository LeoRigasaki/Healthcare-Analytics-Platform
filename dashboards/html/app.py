import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned data
data_path = "./data/processed/cleaned_data_20241226_225801.csv"
df = pd.read_csv(data_path)

# Streamlit App
st.set_page_config(page_title="Healthcare Analytics Dashboard", layout="wide")
st.title("Healthcare Analytics Dashboard")

# Filters
st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox(
    "Select Year:", options=sorted(df["year"].unique()), index=len(df["year"].unique()) - 1
)
selected_category = st.sidebar.selectbox(
    "Select Category:", options=df["category"].unique(), index=0
)

# Filter Data
filtered_df = df[df["year"] == selected_year]
category_df = df[df["category"] == selected_category]

# Bar Chart: Average Data Value by Category
st.subheader("Average Data Value by Category")
bar_chart = px.bar(
    filtered_df.groupby("category", as_index=False)["data_value"].mean(),
    x="category", y="data_value",
    title="Average Data Value by Category",
    labels={"data_value": "Average Data Value"},
)
st.plotly_chart(bar_chart, use_container_width=True)

# Line Chart: Data Value Trends
st.subheader("Data Value Trends Over the Years")
line_chart = px.line(
    category_df,
    x="year", y="data_value", color="stateabbr",
    title=f"Data Value Trends for {selected_category}",
    labels={"data_value": "Data Value"},
)
st.plotly_chart(line_chart, use_container_width=True)

# Pie Chart: Category Distribution
st.subheader("Category Distribution")
pie_chart = px.pie(
    filtered_df, names="category", values="data_value",
    title="Category Distribution",
)
st.plotly_chart(pie_chart, use_container_width=True)

# Scatter Plot: Data Value vs. Total Population
st.subheader("Scatter Plot: Data Value vs. Total Population")
scatter_plot = px.scatter(
    filtered_df,
    x="totalpopulation", y="data_value",
    color="category", size="data_value",
    hover_data=["locationname"],
    title="Data Value vs. Total Population",
    labels={"totalpopulation": "Total Population", "data_value": "Data Value"},
)
st.plotly_chart(scatter_plot, use_container_width=True)
