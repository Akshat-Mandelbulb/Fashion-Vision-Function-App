from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class FashionAnalysisResult:
    """
    Data model for the result of a fashion image analysis.
    """

    primary_color: List[Dict[str, str]] = field(default_factory=list)
    shade: List[str] = field(default_factory=list)
    fabric: List[str] = field(default_factory=list)
    pattern: List[str] = field(default_factory=list)
    description: str = "Fashion item"
    detailed_description: str = "Fashion item - analysis pending"
    tags: List[str] = field(default_factory=lambda: ["fashion", "clothing"])
    colors: List[Dict[str, str]] = field(default_factory=list)
    item_type: List[str] = field(default_factory=lambda: ["clothing"])
    category: List[str] = field(default_factory=lambda: ["clothing"])
    style: List[str] = field(default_factory=lambda: ["casual"])
    season: List[str] = field(default_factory=lambda: ["all-season"])
    occasion: List[str] = field(default_factory=lambda: ["casual"])
    material: List[str] = field(default_factory=lambda: ["unknown"])
    brand: List[str] = field(default_factory=lambda: ["unknown"])

    def model_to_dict(self) -> Dict[str, Any]:
        return asdict(self)
