from fastapi import FastAPI
from mangum import Mangum
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

handler = Mangum(app)