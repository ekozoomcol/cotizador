import os
from fastapi import FastAPI
from pydantic import BaseModel
from app.pricing.engine import quote


app = FastAPI()


@app.get("/ping")
def ping():
    return "pong"


class QuoteRequest(BaseModel):

    bag_type: str
    material: str | None = None
    material_code: str | None = None
    inputs: dict


@app.post("/quote")
def create_quote(req: QuoteRequest):
    material_code = req.material_code or req.material or "CAMBREL_70"

    return quote(
        bag_type=req.bag_type,
        material_code=material_code,
        inputs=req.inputs
    )