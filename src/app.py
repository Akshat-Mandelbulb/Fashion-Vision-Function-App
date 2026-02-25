import json

from azure.functions import AuthLevel, FunctionApp, HttpRequest, HttpResponse

from modules.vision_analysis.vision_analysis_routes import vision_analysis_bp

app = FunctionApp(http_auth_level=AuthLevel.ANONYMOUS)

app.register_blueprint(vision_analysis_bp)


@app.route(route="health", methods=["GET"])
def health_check(req: HttpRequest) -> HttpResponse:
    return HttpResponse(
        json.dumps(
            {
                "status": "healthy",
                "service": "Azure OpenAI Image Analyzer",
                "endpoints": {"analyze": "/api/analyze-image", "health": "/api/health"},
            }
        ),
        status_code=200,
        mimetype="application/json",
    )
