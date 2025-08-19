from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

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
