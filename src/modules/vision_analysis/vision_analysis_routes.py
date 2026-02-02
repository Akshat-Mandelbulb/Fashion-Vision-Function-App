from azure.functions import Blueprint

from modules.vision_analysis.vision_analysis_controller import VisionAnalysisController
from shared.utils.logger_config import setup_logger

logger = setup_logger()

vision_analysis_bp = Blueprint()


@vision_analysis_bp.route(route="analyse-image", methods=["POST"])
async def analyze_image(req):
    logger.info(f"\n==>> req: {req}")
    return await VisionAnalysisController.analyze_image_from_url(req)
