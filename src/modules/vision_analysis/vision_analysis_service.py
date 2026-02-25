import ast
from typing import Dict, Iterable, List

from openai.types.chat import ChatCompletionMessageParam

from modules.vision_analysis.vision_analysis_model import FashionAnalysisResult
from shared.services.azure_openai_service import AzureOpenAIService

FASHION_ANALYSIS_PROMPT = """Act as a fashion analysis API.
Analyze the provided image and return a JSON object strictly following the schema below.
Analyse dress, fashion, style, fabric, pattern, color, shade, occasion, season, material, description, tags, additional colors, brand, detailed description.
Ignore background, environment, people, and other non-fashion elements.
CRITICAL INSTRUCTION: Your response must contain ONLY the JSON object. Do not include markdown code blocks (```json), do not include bold text, and do not include any conversational filler. Start your response with { and end it with }.

{
    "PRIMARY_COLOR": {hex: string, name: string}[],
    "SHADE": [],
    "FABRIC_MATERIAL": [],
    "PATTERN_PRINT": [],
    "CATEGORY": [],
    "ITEM_TYPE": [],
    "STYLE": [],
    "OCCASION": [],
    "SEASON": [],
    "MATERIALS": [],
    "DESCRIPTION": "",
    "TAGS": [],
    "ADDITIONAL_COLORS": {hex: string, name: string}[],
    "BRAND": [],
    "DETAILED_DESCRIPTION": ''
}

Field Specifications:
- PRIMARY_COLOR: Use specific names (e.g., burgundy, teal, charcoal, cream) rather than generic terms.
- SHADE: Specify if the tone is light, dark, pastel, vibrant, or muted.
- FABRIC_MATERIAL: Identify the material (e.g., silk, velvet, cotton).
- PATTERN_PRINT: Detail the design (e.g., embroidered, floral, solid).
- DESCRIPTION: Provide a technical summary of embellishments and aesthetic.
- DETAILED_DESCRIPTION: Provide overall summary of all attributes.
- NO BOLD TEXT: Ensure no values within the JSON contain bold formatting."""


class VisionAnalysisService:
    @classmethod
    async def analyse_image_url(cls, image_url: str) -> FashionAnalysisResult:
        try:
            openai_service = AzureOpenAIService()

            messages: Iterable[ChatCompletionMessageParam] = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": FASHION_ANALYSIS_PROMPT},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ]

            response, tokens_used = await openai_service.chat_completion_text(
                messages=messages
            )

            return cls._parse_azure_function_response(response)
        except Exception as e:
            raise e

    @staticmethod
    def _parse_azure_function_response(analysis_text: str) -> FashionAnalysisResult:
        """Parse Azure Function analysis text into structured metadata"""
        analysis_dict = ast.literal_eval(analysis_text)

        primary_color: List[Dict[str, str]] = analysis_dict.get("PRIMARY_COLOR", [])
        shade: List[str] = analysis_dict.get("SHADE", [])
        fabric: List[str] = analysis_dict.get("FABRIC_MATERIAL", [])
        pattern: List[str] = analysis_dict.get("PATTERN_PRINT", [])
        item_type = analysis_dict.get("ITEM_TYPE", [])
        category = analysis_dict.get("CATEGORY", [])
        colors = analysis_dict.get("ADDITIONAL_COLORS", [])
        style = analysis_dict.get("STYLE", [])
        season = analysis_dict.get("SEASON", [])
        occasion = analysis_dict.get("OCASSION", [])
        material = analysis_dict.get("MATERIALS", [])
        tags = analysis_dict.get("TAGS", [])
        brand = analysis_dict.get("BRAND", [])
        description = analysis_dict.get("DESCRIPTION", "")
        detailed_description = analysis_dict.get("DETAILED_DESCRIPTION", "")

        return FashionAnalysisResult(
            description=description,
            detailed_description=detailed_description,
            tags=tags,
            colors=colors,
            item_type=item_type,
            category=category,
            style=style,
            season=season,
            occasion=occasion,
            material=material,
            brand=brand,
            fabric=fabric,
            pattern=pattern,
            primary_color=primary_color,
            shade=shade,
        )

    def _get_fallback_analysis(self) -> FashionAnalysisResult:
        """Return fallback analysis when Azure Function fails"""
        return FashionAnalysisResult()
