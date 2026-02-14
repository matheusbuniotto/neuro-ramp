# -*- coding: utf-8 -*-
import pytest
from datetime import time
from neuro_ramp.engine import HabitEngine
from neuro_ramp.ui.presenter import UIPresenter

def test_focus_screen_mapping_morning():
    """
    Testa se o estado da UI reflete o pico de cortisol e o load correto.
    """
    engine = HabitEngine()
    presenter = UIPresenter(engine)
    
    habit = engine.initialize_habit("Kettlebell Swings", 50) # Baseline 2.0
    # Simula manhã
    current_time = time(7, 0)
    
    state = presenter.get_focus_state(habit, current_time)
    
    assert state.habit_name == "Kettlebell Swings"
    assert "2.0" in state.current_load_display
    assert state.multiplier_active is True
    assert "CORTISOL" in state.multiplier_label
    assert state.automaticity_percent == pytest.approx(0.0)

def test_automaticity_progress():
    """
    Verifica se o progresso de automaticidade (66 dias) é calculado.
    """
    engine = HabitEngine()
    presenter = UIPresenter(engine)
    habit = engine.initialize_habit("Meditação", 20)
    
    # Simula 33 dias (50% de 66)
    # Como weeks_completed é o que temos, vamos assumir que cada week = 7 dias
    habit.weeks_completed = 4 # ~28 dias
    
    state = presenter.get_focus_state(habit, time(12, 0))
    
    # (4 * 7) / 66 * 100 = 42.42
    assert state.automaticity_percent == pytest.approx(42.42, abs=0.1)
