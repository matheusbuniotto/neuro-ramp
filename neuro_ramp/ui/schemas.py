# -*- coding: utf-8 -*-
from pydantic import BaseModel
from neuro_ramp.engine.habit import ChangeType

class FocusScreenState(BaseModel):
    habit_name: str
    current_load_display: str  # Ex: "14 Swings"
    overload_gauge_percent: float # 0.0 a 100.0
    multiplier_active: bool
    multiplier_label: str | None = None # Ex: "CORTISOL PEAK: 2.3x"
    change_type: str # RAMP, DELOAD, MAINTAIN
    automaticity_percent: float # 0 a 100 (baseado nos 66 dias)
