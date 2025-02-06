from pydantic import BaseModel, HttpUrl

class DivGooglePrices(BaseModel):
    """
    Representa a estrutura de dados de um preço de produto no Google.
    """
    name: str
    location: str
    price: str
    site: HttpUrl 