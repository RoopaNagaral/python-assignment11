import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.data as pldata

# Note, you need to create a 'db' directory if it isn't already in your workspace

DB_PATH = "db/lesson.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
    
conn.execute("PRAGMA foreign_keys = 1;")

try:
    #Task 2: A Line Plot with Pandas
    sql_statement = """
        SELECT o.order_id, SUM(price * quantity) AS total_price 
        FROM orders o JOIN line_items l ON o.order_id = l.order_id 
        JOIN products p ON l.product_id = p.product_id 
        GROUP BY o.order_id;
    """
    df = pd.read_sql_query(sql_statement, conn)
    
    def cumulative(row):
        totals_above = df['total_price'][0:row.name+1]
        return totals_above.sum()

    df['cumulative'] = df.apply(cumulative, axis=1)
    df['cumulative'] = df['total_price'].cumsum()
    
    # Line Plot
    df.plot(x="order_id", y="cumulative", kind="line", title="Cumulative Revenue Over Time", xlabel="Orders", ylabel="Cumulative Revenue", grid=True)
    plt.show()
    
except Exception as e:
    conn.rollback()
    print("Transaction failed:", e)
finally:
    conn.close()