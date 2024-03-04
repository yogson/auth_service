import uvicorn

from api.app import App

if __name__ == "__main__":
    uvicorn.run(App, host="0.0.0.0", port=8001, factory=True)
