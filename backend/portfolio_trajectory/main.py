"""A performant API framework."""

from fastapi import FastAPI


APP_DESCRIPTION = (
    "Portfolio Trajectory is a FastAPI-powered application that runs Monte "
    "Carlo stock market simulations to provide a realistic range of outcomes "
    "for investing and retirement planning. It helps users model market "
    "volatility and assess potential future portfolio performance."
)

app = FastAPI(
    title="Portfolio Trajectory",
    description=APP_DESCRIPTION,
    version="0.1.0",
)


@app.get("/")
def root():
    """Return a welcome message and status for the Portfolio Trajectory API."""
    return {
        "status": "ok",
        "message": "Welcome to Portfolio Trajectory API!",
        "description": APP_DESCRIPTION,
        "version": "0.1.0",
        "docs": "/docs",
    }
