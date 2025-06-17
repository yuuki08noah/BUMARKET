import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from exception.user import UserException
from web import auth, product, user, seller

app = FastAPI()
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(user.router)
app.include_router(seller.router)

@app.exception_handler(UserException)
def school_exception_handler(request: Request, exc: UserException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message
        })

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)