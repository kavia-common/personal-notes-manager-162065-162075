from fastapi import FastAPI
from src.api.app import create_app

# Instantiate the FastAPI app using the factory pattern
app: FastAPI = create_app()
