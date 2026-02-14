# -*- coding: utf-8 -*-
from datetime import time
from neuro_ramp.engine import Habit, HabitEngine, ChangeType
from neuro_ramp.ui.schemas import FocusScreenState

class UIPresenter:
    def __init__(self, engine: HabitEngine):
        self.engine = engine

    def get_focus_state(self, habit: Habit, current_time: time) -> FocusScreenState:
        """
        Transforma o estado do Hábito e o tempo atual em um estado de UI (Focus Screen).
        """
        multiplier = self.engine.get_completion_multiplier(current_time)
        is_morning = multiplier > 1.0
        
        # Cálculo de Automaticidade (Gap de 66 dias)
        days_completed = habit.weeks_completed * 7
        automaticity_percent = min(100.0, round((days_completed / 66.0) * 100, 2))
        
        # Gauge de Overload (Proporção do load atual em relação ao target)
        gauge_percent = min(100.0, round((habit.current_load / habit.target_duration_minutes) * 100, 2))
        
        # Determina o tipo de mudança para a UI (simplificado para o estado atual)
        # Em uma implementação real, isso viria da última transição de load
        change_type = "MAINTAIN"
        
        return FocusScreenState(
            habit_name=habit.name,
            current_load_display=f"{habit.current_load} units",
            overload_gauge_percent=gauge_percent,
            multiplier_active=is_morning,
            multiplier_label=f"CORTISOL PEAK: {multiplier}x NEURAL ENCODING ACTIVE" if is_morning else None,
            change_type=change_type,
            automaticity_percent=automaticity_percent
        )
