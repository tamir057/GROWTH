import uuid
from typing import Optional
from pydantic import BaseModel, Field
import datetime

class Plant(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    min_ph: int = Field(...)
    max_ph: int = Field(...)
    min_ec: int = Field(...)
    max_ec: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Romaine Lettuce",
                "description": "Romaine lettuce, distinguished by its tall, cylindrical heads of crisp leaves, boasts a mild and slightly bitter taste. Ideal for hydroponic cultivation, romaine lettuce is relatively easy to grow in nutrient-rich water solutions, with its well-defined growth stages making it suitable for various hydroponic systems such as nutrient film technique (NFT) or deep water culture (DWC). Its rapid growth, resistance to common pests, and straightforward nutrient requirements contribute to the ease and popularity of hydroponic romaine lettuce cultivation.",
                "min_ph": 5.0,
                "min_ph": 6.0,
                "min_ec": 1.2,
                "max_ec": 1.5
            }
        }

class PlantUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    minpH: Optional[int]
    maxpH: Optional[int]
    minEC: Optional[int]
    maxEC: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "description": "Romaine lettuce is yummy",
                "minpH": 5.9,
                "maxEC": 1.4
            }
        }

class Plot(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    plot_number: int = Field(...)
    plant_id: str = Field(...)
    last_reading: {datetime, int, int} = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "019se121-c05l-4a31-w49c-12238c7e1f6k",
                "plot_number": 1,
                "plant_id": "066de609-b04a-4b30-b46c-32537c7f1f6e", 
                "last_reading": {datetime.datetime.now, 5.3, 1.3}
            }
        }

class PlotUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    minpH: Optional[int]
    maxpH: Optional[int]
    minEC: Optional[int]
    maxEC: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "last_reading": {datetime.datetime.now, 5.7, 1.4}
            }
        }