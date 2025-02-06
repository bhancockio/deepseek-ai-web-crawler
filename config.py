# config.py

BASE_URL = "https://www.google.com/search?sca_esv=fcc8a1ce826a5642&tbm=shop&sxsrf=AHTn8zqrcW-ZlgNBTH2s4gA4yyQT18PFww:1738849575159&q=ra%C3%A7%C3%A3o+pedigree+10kg+ra%C3%A7as+pequenas+po%C3%A7os+de+caldas&tbs=mr:1,local_avail:1,ss:55&sa=X&ved=0ahUKEwjpyPq5l6-LAxVxH7kGHeC4H_sQsysIyQEoAA&biw=1920&bih=961&dpr=1"
CSS_SELECTOR = ".sh-dgr__grid-result"  # Seletor para os resultados de produtos
LOCAL_AVAILABILITY_SELECTOR = ".S7D1Ud"  # Seletor para "RETIRADA NA LOJA"
REQUIRED_KEYS = [
    "name",
    "price",
    "location",
    "site"
]
