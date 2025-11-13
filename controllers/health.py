def register(app):
    @app.get("/health")
    def health():
        return {"status": "Saudavel"}
