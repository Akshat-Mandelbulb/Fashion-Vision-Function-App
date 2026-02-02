from azure.functions import Blueprint

from modules.vision_analysis.vision_analysis_controller import VisionAnalysisController

vision_analysis_bp = Blueprint()


@vision_analysis_bp.route(route="analyse-image", methods=["POST"])
def analyze_image(req):
    print("Analyzing image: ", req)
    return VisionAnalysisController.analyze_image_from_url(req)
