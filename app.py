# app.py
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI(title="DataWise Project API")

@app.get("/query")
async def query(q: str = Query(...)):
    # simple logic to return answer placeholder
    return JSONResponse({"answer": f"You asked: {q}"})
