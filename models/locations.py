from pydantic import BaseModel, HttpUrl

class Locations(BaseModel):
    """
    Representa a estrutura de dados de um local no Google.
    """
    name: str
    rating: float
    reviews: int
    address: str
    hours: str
    phone: str