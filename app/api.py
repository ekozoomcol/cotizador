from fastapi import FastAPI
from pydantic import BaseModel
from app.pricing.engine import quote


app = FastAPI()


class QuoteRequest(BaseModel):

    bag_type: str
    material: str
    inputs: dict


@app.post("/quote")
def create_quote(req: QuoteRequest):

    return quote(
        bag_type=req.bag_type,
        material_code=req.material,
        inputs=req.inputs
    )