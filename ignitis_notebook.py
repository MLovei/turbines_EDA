import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium", auto_download=["html", "ipynb"])


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    from datetime import datetime
    import plotly.express as px
    return mo, np, pd, px


@app.cell
def _(pd):
    xls = pd.ExcelFile("POE_Task.xlsx")
    xls.sheet_names
    return (xls,)


@app.cell
def _(xls):
    df_raw = xls.parse("RawData")
    df_wind_turbine_curve = xls.parse("Contractual Power Curve")
    return df_raw, df_wind_turbine_curve


@app.cell
def _(df_wind_turbine_curve):
    print(df_wind_turbine_curve.head(),"\n")
    print(df_wind_turbine_curve.tail())
    return


@app.cell
def _(df_raw):
    df_raw.info()
    return


@app.cell
def _(df_raw):
    df_raw.describe().T
    return


@app.cell
def _(df_raw, df_wind_turbine_curve, mo, np, pd):
    # Ensure Date is datetime
    df_raw["Date"] = pd.to_datetime(df_raw["Date"])

    # Clean column names
    raw = df_raw.rename(columns={
        "Wind speed": "wind_speed",
        "Power avg [kW]": "power",
    })

    # Prepare contractual curve
    curve_sorted = df_wind_turbine_curve.sort_values("Windspeed [m/s]")
    curve_x = curve_sorted["Windspeed [m/s]"].values
    curve_y = curve_sorted["Power"].values

    # Expected power function
    def expected_power(ws: float) -> float:
        if np.isnan(ws): 
            return np.nan
        if ws <= curve_x[0]:
            return curve_y[0]
        if ws >= curve_x[-1]:
            return curve_y[-1]
        idx = np.searchsorted(curve_x, ws)
        x1, x2 = curve_x[idx-1], curve_x[idx]
        y1, y2 = curve_y[idx-1], curve_y[idx]
        return y1 + (y2 - y1) * (ws - x1) / (x2 - x1)

    # Compute expected power for all rows
    raw["expected_power"] = raw["wind_speed"].apply(expected_power)

    # Operational status function
    def op_status(row):
        if row["power"] == 0 and row["wind_speed"] >= 3:
            return "Stop/Maintenance"
        if row["wind_speed"] < 3:
            return "Below cut-in"
        if row["wind_speed"] > 15 and row["power"] < 0.1:
            return "High wind stop"
        return "Normal operation"

    # Apply operational status
    raw["status"] = raw.apply(op_status, axis=1)

    # Show data info
    mo.md(f"📊 Data loaded: {len(raw)} records from {raw['Date'].min().date()} to {raw['Date'].max().date()}")

    return curve_sorted, raw


@app.cell
def _(curve_sorted, mo, pd, px):
    def filter_data(df: pd.DataFrame, d1, d2, w1, w2):
        # Convert dates back to datetime for comparison
        d1 = pd.to_datetime(d1)
        d2 = pd.to_datetime(d2)
    
        # Apply filters
        mask = (df["Date"] >= d1) & (df["Date"] <= d2)
        mask &= (df["wind_speed"] >= w1) & (df["wind_speed"] <= w2)
    
        return df.loc[mask].copy()

    def build_fig(filtered_df, color_column, opacity_val, show_curve_flag):
        # Create scatter plot
        fig = px.scatter(
            filtered_df,
            x="wind_speed",
            y="power",
            color=color_column,
            opacity=opacity_val,
            labels={
                "wind_speed": "Wind speed (m/s)", 
                "power": "Normalized power"
            },
            title="🔋 Power Curve Analysis: Actual vs Contractual Performance",
            hover_data=["Date", "expected_power", "status"]
        )

        # Add contractual curve if enabled
        if show_curve_flag:
            fig.add_scatter(
                x=curve_sorted["Windspeed [m/s]"],
                y=curve_sorted["Power"],
                mode="lines",
                name="Contractual power curve",
                line=dict(color="black", width=3, dash="dash")
            )

        # Update layout
        fig.update_layout(
            legend_title_text="",
            template="plotly_white",
            margin=dict(l=10, r=10, t=50, b=10),
            height=600,
            xaxis_title="Wind Speed (m/s)",
            yaxis_title="Normalized Power Output"
        )
    
        return fig

    mo.md("✅ Helper functions defined")

    return build_fig, filter_data


@app.cell
def _(
    build_fig,
    color_by,
    date_range,
    filter_data,
    opacity,
    raw,
    show_curve,
    wind_range,
):
    # Get current UI values
    d1, d2 = date_range.value
    w1, w2 = wind_range.value
    color_arg = None if color_by.value == "None" else color_by.value

    # Filter data based on UI inputs
    filtered = filter_data(raw, d1, d2, w1, w2)

    # Build and display the figure
    power_fig = build_fig(filtered, color_arg, opacity.value, show_curve.value)

    # Display stats and chart
    stats_md = f"""
    ### 📊 Filtered Data Statistics
    - **Records shown**: {len(filtered):,}
    - **Date range**: {d1} to {d2}
    - **Wind range**: {w1:.1f} - {w2:.1f} m/s
    - **Status distribution**:
    """

    if len(filtered) > 0:
        status_counts = filtered["status"].value_counts()
        for status, count in status_counts.items():
            pct = (count / len(filtered)) * 100
            stats_md += f"\n  - {status}: {count} ({pct:.1f}%)"
    else:
        stats_md += "\n  - No data in selected range"
    return power_fig, stats_md


@app.cell
def _(mo, raw):
    # UI Controls
    date_min = raw["Date"].min().date()
    date_max = raw["Date"].max().date()
    wind_min = float(raw["wind_speed"].min())
    wind_max = float(raw["wind_speed"].max())

    date_range = mo.ui.date_range(
        label="📅 Date range",
        value=[date_min, date_max],
        start=date_min,
        stop=date_max,
    )

    wind_range = mo.ui.range_slider(
        label="💨 Wind speed filter (m/s)",
        start=wind_min, 
        stop=wind_max,
        step=0.1,
        value=[wind_min, wind_max]
    )

    color_by = mo.ui.dropdown(
        label="🎨 Color by",
        options=["status", "None"],
        value="status",
    )

    opacity = mo.ui.slider(
        label="👁️ Point opacity",
        start=0.1, 
        stop=1.0, 
        step=0.1, 
        value=0.6
    )

    show_curve = mo.ui.checkbox(
        label="📈 Show contractual curve",
        value=True
    )

    # Display controls
    mo.vstack([
        mo.hstack([date_range, wind_range]),
        mo.hstack([color_by, opacity, show_curve]),
    ])

    return color_by, date_range, opacity, show_curve, wind_range


@app.cell
def _(power_fig):
    power_fig
    return


@app.cell
def _(mo, stats_md):
    mo.md(stats_md)
    return


if __name__ == "__main__":
    app.run()
