from fastapi import Form
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, field_validator
from uuid import UUID

class ProjectRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    priority_type_id: UUID
    manager_id: UUID
    group_id: UUID | None = None


    # Parsear multipart -> modelo
    @classmethod
    def as_form(
        cls,
        id: UUID = Form(...),
        name: str = Form(...),
        priority_type_id: UUID = Form(...),
        manager_id: UUID = Form(...),
        group_id: UUID | None = Form(None),

    ) -> "ProjectRequest":
        return cls(
            id=id,
            name=name,
            priority_type_id=priority_type_id,
            manager_id=manager_id,
            group_id=group_id,
        )
