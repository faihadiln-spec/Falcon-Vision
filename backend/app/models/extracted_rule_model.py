from pydantic import BaseModel, Field

from app.core.constants import EntityStatus, RuleCategory, Severity, VisionModule
from app.models.base import PyObjectId, TenantModel


class RuleApplicability(BaseModel):
    zone_types: list[str] = Field(default_factory=list)
    employee_roles: list[str] = Field(default_factory=list)
    camera_tags: list[str] = Field(default_factory=list)


class VisionRuleMapping(BaseModel):
    module: VisionModule
    required_classes: list[str] = Field(default_factory=list)
    violation_when: str
    confidence_threshold: float = Field(default=0.75, ge=0, le=1)


class RuleSource(BaseModel):
    page_number: int | None = None
    text_excerpt: str | None = None


class ExtractedRuleModel(TenantModel):
    regulation_id: PyObjectId
    rule_code: str
    title: str
    description: str
    category: RuleCategory
    severity: Severity
    applies_to: RuleApplicability = Field(default_factory=RuleApplicability)
    vision_mapping: VisionRuleMapping
    source: RuleSource = Field(default_factory=RuleSource)
    status: EntityStatus = EntityStatus.ACTIVE
