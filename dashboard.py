
import streamlit as st
import pandas as pd
import pyodbc

st.set_page_config(
    page_title="Sales Data Warehouse",
    page_icon="📊",
    layout="wide"
)

st.title("Sales Data Warehouse Dashboard")
st.caption("Local data engineering portfolio project")

SERVER = ".\SQLSERVERSS"

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={SERVER};"
    "DATABASE=SalesWarehouse;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

@st.cache_data(ttl=60)
def load_sales():
    with pyodbc.connect(CONNECTION_STRING) as conn:
        return pd.read_sql(
            """
            SELECT order_id, customer, product, quantity,
                   unit_price, total_amount, loaded_at
            FROM dbo.FactSales
            ORDER BY order_id
            """,
            conn
        )

try:
    sales = load_sales()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Orders", f"{len(sales):,}")
    col2.metric(
        "Total Sales",
        f"${sales['total_amount'].sum():,.2f}"
    )
    col3.metric(
        "Average Order Value",
        f"${sales['total_amount'].mean():,.2f}"
    )

    st.subheader("Sales by Product")
    product_sales = (
        sales.groupby("product", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
    )
    st.bar_chart(
        product_sales,
        x="product",
        y="total_amount"
    )

    st.subheader("Sales Records")
    st.dataframe(sales, use_container_width=True)

    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()

except Exception as error:
    st.error("Could not connect to SQL Server.")
    st.code(str(error))
    st.info(
        "Check YOUR_SQL_SERVER_NAME and make sure "
        "your SQL Server instance is running."
    )
