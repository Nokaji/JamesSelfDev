from configManager import ConfigManager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

class API:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.app = FastAPI()
        return
    
    def initRouter (self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self.app.add_middleware(HTTPSRedirectMiddleware)
        self.app.add_middleware(AuthenticationMiddleware)
        
        @self.app.get("/")
        async def root():
            return {"message": "Welcome to the API!"}

        print("API initialized with CORS, HTTPS redirect, and authentication middleware.")

if __name__ == "__main__":
    api = API()