from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/api/")
async def process_file(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}
