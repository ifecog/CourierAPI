from fastapi import FastAPI
from app.routes import couriers, packages

app = FastAPI(
    title='CLRD Courier API',
    description='A CRUD API for courier management',
    version='1.0.0'
)

app.include_router(couriers.router, prefix='/couriers', tags=['Couriers'])
app.include_router(packages.router, prefix='/packages', tags=['Couriers'])

app.get('/')
async def root():
    return {'message': 'Welcome to CLRD Courier API'}