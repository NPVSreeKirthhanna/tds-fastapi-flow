from fastapi import FastAPI, Query, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import matplotlib.pyplot as plt
import io, base64, os

app = FastAPI(title="TDS FastAPI Flow")

# Handle root GET
@app.get("/")
async def root():
    return {"status": "ok", "message": "API is running"}

# Handle root POST
@app.post("/")
async def root_post():
    return {"status": "ok", "message": "POST received at root"}

# Actual query endpoint
@app.get("/query")
async def query(q: str = Query(...)):
    return JSONResponse({"answer": f"You asked: {q}"})


# NEW: Upload and generate chart
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    try:
        if ext == ".csv":
            df = pd.read_csv(file.file)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file.file)
        else:
            return JSONResponse({"error": f"Unsupported file format: {ext}"})
    except Exception as e:
        return JSONResponse({"error": f"Could not read file: {str(e)}"})

    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        return JSONResponse({"summary": "No numeric columns found", "chart": None})

    ycol = numeric_cols[0]
    xcol = df.columns[0] if df.columns[0] != ycol else df.index

    fig, ax = plt.subplots()
    ax.plot(df[xcol], df[ycol], marker="o")
    ax.set_title(f"{ycol} over {xcol}")
    ax.set_xlabel(str(xcol))
    ax.set_ylabel(str(ycol))

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    chart_b64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)

    return JSONResponse({
        "rows": len(df),
        "columns": list(df.columns),
        "chart": chart_b64
    })
