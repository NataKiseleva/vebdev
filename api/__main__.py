import uvicorn

uvicorn.run(
    'api.service:app',
    host='0.0.0.0',
    port=5000,
    reload=True
)