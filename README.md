# Quickstart Guide: Ignitis Renewables Marimo Notebook

This guide shows how to set up and run the Marimo notebook using Poetry for dependency management.

## Prerequisites

- Git (optional)
- Python 3.8+
- Poetry installed ([https://python-poetry.org](https://python-poetry.org))


## 1. Clone or Download Repository

```bash
git clone https://github.com/MLovei/turbines_EDA
cd turbines_EDA
```

Or simply place the files (`pyproject.toml`, `ignitis_notebook.py`, `POE_Task.xlsx`) in a project folder.

## 2. Install Dependencies

Use Poetry to install all required packages:

```bash
poetry install
```

This reads `pyproject.toml` (and `poetry.lock` if present) to create a virtual environment and install:

- marimo
- pandas
- numpy
- plotly
- other project dependencies


## 3. Activate Poetry Shell

Spawn a shell with the virtual environment:

```bash
poetry shell
```

You should see your prompt prefixed with the environment name.

## 4. Launch Marimo Notebook

Run the Marimo notebook server:

```bash
marimo notebook
```

This opens a browser window or tab. Navigate to the file:

```
ignitis_notebook.py
```


## 5. Place the Excel File

Ensure the turbine data file is next to the notebook:

```
POE_Task.xlsx
ignitis_notebook.py
```


## 6. Run the Notebook

1. **Cell 1** – Data Loading \& Preparation
2. **Cell 2** – UI Controls
3. **Cell 3** – Helper Functions
4. **Cell 4** – Interactive Chart
5. **Cell 5** – Performance Summary

Execute each cell in order. After adjusting filters in Cell 2, **re-run Cells 4 \& 5** to update.

## 7. Customize \& Explore

- Filter by date range and wind speed
- Toggle contractual curve visibility
- Color by operational status
- Inspect statistics and deviation metrics


## 8. Exit

When finished, exit the Poetry shell:

```bash
exit
```

And stop the Marimo server with `Ctrl+C` in the terminal.

***

You’re now ready to interactively explore wind turbine performance with Marimo and Poetry!

