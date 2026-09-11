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
    df.plot(x="order_id", y=["cumulative"], kind="line", title="Cumulative revenue vs. Order_id")
    plt.show()
    
    #Task 3: Interactive Visualizations with Plotly
    df = pldata.wind(return_type='pandas')
    print("First 10 rows of DataFrame:")
    print(df.head(10))
    
    print("\nLast 10 rows of DataFrame:")
    print(df.tail(10))
    
    df['strength'] = (
        df['strength']
        .str.replace(r'[^0-9\.]', '', regex=True)   # remove anything that's not a digit or dot
        .astype(float)                              # convert to float
    )
    
    #df = pldata.iris(return_type='pandas') # Returns a DataFrame.  plotly.data has a number of sample datasets included.
    fig = px.scatter(df, x='strength', y='frequency', color="direction", title="Strength vs Frequency by Direction", labels={"strength":"Strength", "frequency":"Frequency"})
    fig.write_html("wind.html", auto_open=True)    
         
except Exception as e:
    conn.rollback()
    print("Transaction failed:", e)
finally:
    conn.close()