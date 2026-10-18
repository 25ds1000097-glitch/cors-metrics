import time
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

EMAIL = "25ds1000097@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-35ekcs.example.com"

app = FastAPI()

# Bouncer #1: CORS. Only ONE origin is allowed, never "*".
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)

# Bouncer #2: stamp every response with an ID and a timer.
# This is added AFTER the CORS middleware, so it wraps it and also
# stamps preflight (OPTIONS) replies.
@app.middleware("http")
async def add_headers(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


@app.get("/stats")
def stats(values: str = ""):
    nums = [int(v) for v in values.split(",") if v.strip() != ""]
    if not nums:
        return {"email": EMAIL, "count": 0, "sum": 0,
                "min": None, "max": None, "mean": 0.0}
    total = sum(nums)
    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / len(nums),
    }
