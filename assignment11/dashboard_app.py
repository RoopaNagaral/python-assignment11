import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# Sample data
np.random.seed(42)
df = pd.DataFrame({
"Product": ["Product A", "Product B", "Product C", "Product D"],
"Sales": np.random.randint(100, 500, size=4),
"Profit": np.random.randint(20, 100, size=4)
})
st.title("Product Dashboard")

# Sidebar
st.sidebar.header("Filter Options")
selected = st.sidebar.selectbox("Select Product", df["Product"])
# Filter the data
filtered = df[df["Product"] == selected]

col1, col2 = st.columns(2)
with col1:
    st.metric("Sales", f"${filtered['Sales'].values[0]:,}")
with col2:
    st.metric("Profit", f"${filtered['Profit'].values[0]:,}")
    
st.subheader("Sales and Profit Comparison")
fig = px.bar(df, x="Product", y=["Sales", "Profit"],
barmode="group")
st.plotly_chart(fig)

with st.expander("View Raw Data"):
    st.dataframe(df)
    
min_sales = st.sidebar.slider("Min Sales", 0,500,100)
multi_select = st.sidebar.multiselect("Products", df["Product"])
show_profit = st.checkbox("Show profit")