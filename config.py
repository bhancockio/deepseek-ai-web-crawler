# config.py

BASE_URL = "https://www.google.com/search?sca_esv=fcc8a1ce826a5642&tbm=lcl&sxsrf=AHTn8zqTqEL-62YQaL5AK7PrFnYSJGTfWA:1738851736363&q=pet+shop+po%C3%A7os+de+caldas&rflfq=1&num=10&sa=X&ved=2ahUKEwi0_b_An6-LAxVwsJUCHbbyMTMQjGp6BAgnEAE&biw=1920&bih=961&dpr=1"

# Seletores para extrair informações dos pet shops
CSS_SELECTOR = ".rllt__details"  # Seletor para cada resultado de pet shop
NAME_SELECTOR = ".OSrXXb"  # Nome do pet shop
RATING_SELECTOR = ".yi40Hd"  # Avaliação 
REVIEWS_SELECTOR = ".RDApEe"  # Número de avaliações
ADDRESS_SELECTOR = "div:nth-child(3)"  # Endereço 
HOURS_SELECTOR = "div:nth-child(4)"  # Horário de funcionamento
PHONE_SELECTOR = "div:nth-child(4)"  # Telefone (na mesma div dos horários)

PAGINATION_SELECTOR = ".fl"  # Seletor para botões de paginação
NEXT_PAGE_SELECTOR = "#pnnext"  # Seletor para próxima página

REQUIRED_KEYS = [
    "name", 
    "rating", 
    "reviews", 
    "address", 
    "hours", 
    "phone"
]
