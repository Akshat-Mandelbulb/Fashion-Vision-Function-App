import azure.functions as func
import logging
import json
from openai import AzureOpenAI
import os
from datetime import datetime

# Initialize Azure Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Azure OpenAI Configuration
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT") or ""
AZURE_API_KEY = os.getenv("AZURE_API_KEY") or ""
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME") or ""

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    api_version=os.getenv("API_VERSION") or "",
    azure_endpoint=AZURE_ENDPOINT
)


def analyze_image_from_url(image_url, prompt):
    """
    Analyze an image from a URL (including blob URLs with SAS tokens)
    """
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content, None
   
    except Exception as e:
        error_message = str(e)
        if "content_filter" in error_message:
            return None, "content_filter"
        else:
            return None, error_message


def analyze_fashion_item(image_url, custom_prompt=None):
    """
    Analyze fashion item with structured prompt
    """
    # Default structured prompt
    primary_prompt = custom_prompt or """
    Provide a detailed product analysis in the following format:
   
    1. Product Category: Type of item
    2. Color Scheme: Colors present
    3. Fabric Type: Material composition
    4. Design Elements: Patterns and features
    5. Construction: Design characteristics
    6. Use Context: Suitable settings
   
    Provide objective specifications.
    """
   
    # Fallback prompt
    fallback_prompt = "Describe this product objectively, focusing on color, material, and design features."
   
    # Try primary prompt
    result, error = analyze_image_from_url(image_url, primary_prompt)
   
    # If content filter triggered, try fallback
    if error == "content_filter":
        logging.warning("Primary analysis blocked by content policy. Trying fallback...")
        result, error = analyze_image_from_url(image_url, fallback_prompt)
   
    return result, error


@app.route(route="analyze-image", methods=["POST", "GET"])
def analyze_image(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function to analyze images using Azure OpenAI GPT-4o
    
    Expected Input (JSON):
    {
        "image_url": "https://yourstorageaccount.blob.core.windows.net/container/image.jpg?sv=2021-06-08&ss=...",
        "prompt": "Optional custom prompt"
    }
    
    Or Query Parameters:
    ?image_url=<blob_url>&prompt=<optional_prompt>
    """
    logging.info('Image analysis function triggered.')
    
    try:
        # Extract parameters from request
        image_url = None
        custom_prompt = None
        
        # Try to get from query parameters first
        image_url = req.params.get('image_url')
        custom_prompt = req.params.get('prompt')
        
        # If not in query params, try request body
        if not image_url:
            try:
                req_body = req.get_json()
                image_url = req_body.get('image_url')
                custom_prompt = req_body.get('prompt')
            except ValueError:
                pass
        
        # Validate input
        if not image_url:
            return func.HttpResponse(
                json.dumps({
                    "error": "Missing required parameter",
                    "message": "Please provide 'image_url' in the request body or query parameters",
                    "example": {
                        "image_url": "https://yourstorageaccount.blob.core.windows.net/container/image.jpg?sv=...",
                        "prompt": "Optional custom prompt"
                    }
                }),
                status_code=400,
                mimetype="application/json"
            )
        
        logging.info(f'Analyzing image from URL: {image_url[:50]}...')
        
        # Analyze the image
        result, error = analyze_fashion_item(image_url, custom_prompt)
        
        # Handle errors
        if error == "content_filter":
            return func.HttpResponse(
                json.dumps({
                    "error": "Content filter triggered",
                    "message": "This image triggered Azure's content filtering policy",
                    "suggestions": [
                        "Try a different image (product-only, flat lay, or mannequin)",
                        "Ensure image is appropriate product photography",
                        "Contact Azure admin to adjust content filter settings"
                    ]
                }),
                status_code=400,
                mimetype="application/json"
            )
        elif error:
            return func.HttpResponse(
                json.dumps({
                    "error": "Analysis failed",
                    "message": error
                }),
                status_code=500,
                mimetype="application/json"
            )
        
        # Return successful response
        response_data = {
            "success": True,
            "image_url": image_url[:100] + "..." if len(image_url) > 100 else image_url,
            "analysis": result,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        logging.info('Image analysis completed successfully.')
        
        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logging.error(f'Error processing request: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "message": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="health", methods=["GET"])
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """
    Health check endpoint
    """
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "service": "Azure OpenAI Image Analyzer",
            "endpoints": {
                "analyze": "/api/analyze-image",
                "health": "/api/health"
            }
        }),
        status_code=200,
        mimetype="application/json"
    )