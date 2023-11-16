from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Plant, PlantUpdate, Plot, PlotUpdate

router = APIRouter()

@router.post("/", response_description="Create a new plant", status_code=status.HTTP_201_CREATED, response_model=Plant)
def create_plant(request: Request, plant: Plant = Body(...)):
    plant = jsonable_encoder(plant)
    new_plant = request.app.database["plants"].insert_one(plant)
    created_plant = request.app.database["plants"].find_one(
        {"_id": new_plant.inserted_id}
    )

    return created_plant

@router.post("/", response_description="Create a new plot", status_code=status.HTTP_201_CREATED, response_model=Plot)
def create_book(request: Request, plot: Plot = Body(...)):
    plot = jsonable_encoder(plot)
    new_plot = request.app.database["plots"].insert_one(plot)
    created_plot = request.app.database["plots"].find_one(
        {"_id": new_plot.inserted_id}
    )

    return created_plot

@router.get("/", response_description="List all plants", response_model=List[Plant])
def list_plants(request: Request):
    plants = list(request.app.database["plants"].find(limit=100))
    return plants

@router.get("/", response_description="List all plots", response_model=List[Plot])
def list_plots(request: Request):
    plots = list(request.app.database["plots"].find(limit=100))
    return plots