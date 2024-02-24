import uvicorn

from .settings import settings

print("main")

uvicorn.run(
    'workshop.app:app',
    reload=True,
)
