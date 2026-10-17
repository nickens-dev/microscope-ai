from fastapi import FastAPI

app = FastAPI(
    title="Microscope AI API",
    version="1.0.0"
)

@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}