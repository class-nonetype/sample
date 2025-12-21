from src.api.application import get_application
from src.utils.properties import API_HOST, API_PORT
from uvicorn import run

def run_server():
    run(app=get_application(), host=API_HOST, port=API_PORT)