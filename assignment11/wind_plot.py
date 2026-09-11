import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.data as pldata
import webbrowser

# Note, you need to create a 'db' directory if it isn't already in your workspace

DB_PATH = "db/lesson.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
    
conn.execute("PRAGMA foreign_keys = 1;")

try:
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
    # --- Save HTML file in assignment11 folder ---
    output_path = "wind.html"
    fig.write_html(output_path, include_plotlyjs="cdn")

    print(f"Saved interactive plot to {output_path}")

    # --- Load/verify by opening in browser ---
    abs_path = os.path.abspath(output_path)
    webbrowser.open(f"file://{abs_path}")
    
except Exception as e:
    conn.rollback()
    print("Transaction failed:", e)
finally:
    conn.close()