import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api:app", log_level="debug", reload=True)
