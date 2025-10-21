import uvicorn

from app.main import create_app

app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=app.state.settings.app.HOST,
        port=app.state.settings.app.PORT,
        reload=True,
        reload_dirs=["src"],
    )
