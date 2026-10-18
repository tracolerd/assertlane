from fastapi import FastAPI
app = FastAPI(
    title="AssertLane API",
    description="Quality Engineering Platform API",
    version="0.1.0"
)
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "AssertLane backend is operational"}
