from configManager import ConfigManager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from datetime import datetime

class API:
    def __init__(self):
        self.startTime = datetime.now()
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

        if(self.config_manager.config["environment"] == "production"):
            self.app.add_middleware(AuthenticationMiddleware)
            self.app.add_middleware(HTTPSRedirectMiddleware)

        from routes.crew_router import crew_router
        self.app.include_router(crew_router, prefix="/crew", tags=["crew"])

        @self.app.get("/")
        async def root():
            return {"message": "Welcome to the SelfDevelopment API!",
                    "endpoint": [route.path for route in self.app.routes]}

        print("API initialized with CORS, HTTPS redirect, and authentication middleware.")

if __name__ == "__main__":
    api = API()
    api.initRouter()
    import uvicorn
    uvicorn.run(api.app, host=api.config_manager.config['host'], port=api.config_manager.config['port'])
    print(f"API running on {api.config_manager.config['host']}:{api.config_manager.config['port']}")