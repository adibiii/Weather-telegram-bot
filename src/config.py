from datetime import datetime

a = datetime.now()

date = a.strftime("%Y-%m-%d")

BASE_PATH = """https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"""

LOCATION_AND_DATE = f"marivan,iran/{date}?"

API_KEY = "key=USP7YWE8YG92JG4BB3VPHZHDS"

API_OPTION = "&include=days"

API_ELEMENTS = "&elements=datetime,temp"


url = BASE_PATH+LOCATION_AND_DATE+API_KEY+API_OPTION

TOKEN = "7079971599:AAFgAxDjkpLK8pakiMf5k-5QzmLN5YNYVkY"
