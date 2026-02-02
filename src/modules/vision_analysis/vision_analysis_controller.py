import json
import re
from http import HTTPStatus

from azure.functions import HttpRequest, HttpResponse

from modules.vision_analysis.vision_analysis_service import VisionAnalysisService
from shared.utils.constants import URL_REGEX
from shared.utils.exceptions import InvalidRequestError


class VisionAnalysisController:
    @staticmethod
    async def analyze_image_from_url(req: HttpRequest):
        """
        Expected Input (JSON):
        {
            "image_url": "https://yourstorageaccount.blob.core.windows.net/container/image.jpg?sv=2021-06-08&ss=..."
        }
        """
        try:
            image_url = req.params.get("image_url")
            if not image_url or not re.search(URL_REGEX, image_url):
                raise InvalidRequestError()

            result = await VisionAnalysisService.analyse_image_url(image_url)

            return HttpResponse(
                json.dumps({"success": True, "data": result.model_to_dict()}),
                status_code=200,
                mimetype="application/json",
            )
        except InvalidRequestError as e:
            return HttpResponse(
                json.dumps({"success": False, "message": e.message}),
                status_code=(
                    e.status_code if e.status_code else HTTPStatus.INTERNAL_SERVER_ERROR
                ),
                mimetype="application/json",
            )
        except Exception as e:
            return HttpResponse(
                json.dumps({"success": False, "error": str(e)}),
                status_code=500,
                mimetype="application/json",
            )
