import uvicorn
import load_env
from app.app import create_app
from app.Core.config import settings

app = create_app()

if __name__ == '__main__':
    print("Starting server...")
    uvicorn.run("main:app", host=settings.HOST_URL, port=settings.HOST_PORT, reload=True)