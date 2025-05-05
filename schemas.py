from pydantic import BaseModel, Field, field_validator
from typing import Literal

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class NDResult(BaseModel):
    nom_det_tag: Literal["Yes", "No"] = Field(
        ..., description="‘Yes’ if the name semantically matches the job, otherwise ‘No’"
    )
    nom_det_explain: str = Field(
        ..., max_length=500,
        description="A 2-3 line explanation of your decision"
    )

    @field_validator("nom_det_explain")
    def explain_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Explanation must be non-empty")
        return v
