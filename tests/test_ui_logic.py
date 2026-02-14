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
    assert state.theme_color == "#00FF41" # Maintain default
    assert state.haptic_feedback == "heavy"

def test_focus_screen_mapping_deload():
    """
    Verifica se o tema muda para Cyber-Orange durante um deload.
    """
    engine = HabitEngine()
    presenter = UIPresenter(engine)
    habit = engine.initialize_habit("Musculação", 60)
    
    # Força um deload
    habit.weeks_completed = 4
    engine.apply_next_week_load(habit, 0.9) # Próxima semana é a 5ª
    
    state = presenter.get_focus_state(habit, time(12, 0))
    
    assert state.change_type.name == "DELOAD"
    assert state.theme_color == "#FF9100" # Cyber-Orange
    assert state.haptic_feedback == "warning"

def test_automaticity_progress():
    """
    Verifica se o progresso de automaticidade (66 dias) é calculado.
    """
    engine = HabitEngine()
    presenter = UIPresenter(engine)
    habit = engine.initialize_habit("Meditação", 20)
    
    # Simula 33 dias (50% de 66)
    habit.days_completed = 33
    
    state = presenter.get_focus_state(habit, time(12, 0))
    
    assert state.automaticity_percent == pytest.approx(50.0)
