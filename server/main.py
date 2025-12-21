#from src.api.server import run_server

#if __name__ == '__main__':
#    run_server()


# python -m uvicorn main:app --host localhost --port 8000 --reload --use-colors

from src.api.application import get_application

app = get_application()