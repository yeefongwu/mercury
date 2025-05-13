import json
import os
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Query
from typing import List
from models import Premium
from generator import PremiumGenerator
from comparator import PremiumComparator
from validator import PremiumValidator

app = FastAPI(
    title="Insurance Premium API",
    description="API for insurance premium operations",
    version="1.0.0"
)

@app.get("/premiums/generate", response_model=List[Premium])
async def generate_premiums(count: int = Query(1, ge=1, le=100)):
    if os.path.exists("premiums.json"):
        with open("premiums.json", "r") as json_file:
            premiums = json.load(json_file)
    else:
        premiums = []

    new_premiums = [PremiumGenerator.generate_premium() for _ in range(count)]
    premiums.extend([premium.dict() for premium in new_premiums]) 

    with open("premiums.json", "w") as json_file:
        json.dump(premiums, json_file, indent=2)

    return new_premiums


@app.post("/premiums/compare")
async def compare_premiums(id1: str, id2: str, tolerance: float = 0.01):
    if not os.path.exists("premiums.json"):
        return {"error": "Premiums file not found"}  

    with open("premiums.json", "r") as json_file:
        premiums = json.load(json_file)

    premium1 = next((premium for premium in premiums if premium["id"] == id1), None)
    premium2 = next((premium for premium in premiums if premium["id"] == id2), None)

    if premium1 is None or premium2 is None:
        return {"error": "One or both premiums not found"}  

    are_equal = PremiumComparator.are_equal(premium1, premium2, tolerance)

    return {
        "are_equal": are_equal
    }

@app.post("/premiums/validate")
async def validate_premium(id: str):
    with open("premiums.json", "r") as json_file:
        premiums = json.load(json_file)
    premium = next((premium for premium in premiums if premium["id"] == id), None)
    errors = PremiumValidator.validate_with_errors(premium)
    return {"is_valid": not errors, "errors": errors}