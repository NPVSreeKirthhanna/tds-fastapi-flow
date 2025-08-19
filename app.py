# app.py
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/query")
async def query(q: str = Query(...)):
    # Simple placeholder
    return JSONResponse({"answer": f"You asked: {q}"})
