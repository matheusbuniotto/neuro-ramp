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
        # Prioriza days_completed se estiver populado, caso contrário usa semanas
        days = habit.days_completed if habit.days_completed > 0 else (habit.weeks_completed * 7)
        automaticity_percent = min(100.0, round((days / 66.0) * 100, 2))
        
        # Gauge de Overload (Proporção do load atual em relação ao target)
        gauge_percent = min(100.0, round((habit.current_load / habit.target_duration_minutes) * 100, 2))
        
        # Mapeamento de Visual Identity (DESIGN_SPEC.md)
        theme_map = {
            ChangeType.RAMP: ("#00E5FF", "success"),     # Hyper-Blue
            ChangeType.DELOAD: ("#FF9100", "warning"),   # Cyber-Orange
            ChangeType.MAINTAIN: ("#00FF41", "heavy")    # Neon Green
        }
        
        color, haptic = theme_map.get(habit.last_change, ("#00FF41", "heavy"))

        return FocusScreenState(
            habit_name=habit.name,
            current_load_display=f"{habit.current_load} units",
            overload_gauge_percent=gauge_percent,
            multiplier_active=is_morning,
            multiplier_label=f"CORTISOL PEAK: {multiplier}x NEURAL ENCODING ACTIVE" if is_morning else None,
            change_type=habit.last_change,
            automaticity_percent=automaticity_percent,
            theme_color=color,
            haptic_feedback=haptic
        )
