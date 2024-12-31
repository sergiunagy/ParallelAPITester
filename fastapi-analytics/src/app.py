from fastapi import FastAPI
from routes import testroutes

app = FastAPI()

# connect the routes
app.include_router(testroutes.router)# should be available in test mode only 
