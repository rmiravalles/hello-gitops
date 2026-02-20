from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Howdy Ho! This is GitOps with Flux 🚀"}