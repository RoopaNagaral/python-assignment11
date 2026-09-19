import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.data as pldata
from pathlib import Path

try:
    #Task 3: Interactive Visualizations with Plotly
    df = pldata.wind(return_type='pandas')
    print("First 10 rows of DataFrame:")
    print(df.head(10))
    
    print("\nLast 10 rows of DataFrame:")
    print(df.tail(10))
    
    df['strength'] = (
        df['strength']
        .str.replace(r"-.*$|\+$", '', regex=True)   # remove anything that's not a digit or dot
        .astype(float)                              # convert to float
    )
    
    #df = pldata.iris(return_type='pandas') # Returns a DataFrame.  plotly.data has a number of sample datasets included.
    fig = px.scatter(df, x='strength', y='frequency', color="direction", title="Strength vs Frequency by Direction", labels={"strength":"Strength", "frequency":"Frequency"})
   
    # --- Save HTML file in assignment11 folder ---
    output_path = output_path = Path(__file__).resolve().parent / "wind.html"
    fig.write_html(output_path, include_plotlyjs=True, auto_open=True)

    print(f"Saved interactive plot to {output_path}")
    
except Exception as e:
    print("Transaction failed:", e)
