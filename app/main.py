from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Howdy Ho and Behold! GitOps with Flux is in the house 🚀"}