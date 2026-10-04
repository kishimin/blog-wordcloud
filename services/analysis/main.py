from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import analyze


app = FastAPI()


origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"message": "OK"}


app.include_router(analyze.router)
