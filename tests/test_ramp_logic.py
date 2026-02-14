# -*- coding: utf-8 -*-
import pytest
from neuro_ramp.engine import HabitEngine, Habit

def test_weekly_ramp_calculation_success():
    """
    Testa se o load aumenta em 15% quando a aderência é > 80%.
    """
    engine = HabitEngine()
    # Inicializa com 10 minutos (baseline será 2.0)
    habit = engine.initialize_habit("Exercício", 10.0)
    
    initial_load = habit.current_load # 2.0
    adherence_rate = 0.85 # 85% (> 80%)
    
    new_load = engine.calculate_next_week_load(habit, adherence_rate)
    
    # 2.0 * 1.15 = 2.3
    assert new_load == pytest.approx(initial_load * 1.15)

def test_weekly_ramp_failure_low_adherence():
    """
    Testa se o load NÃO aumenta quando a aderência é <= 80%.
    """
    engine = HabitEngine()
    habit = engine.initialize_habit("Exercício", 10.0)
    
    initial_load = habit.current_load
    adherence_rate = 0.70 # 70% (<= 80%)
    
    new_load = engine.calculate_next_week_load(habit, adherence_rate)
    
    # Deve manter o load atual ou até reduzir (mas por enquanto, manter)
    assert new_load == initial_load

def test_weekly_ramp_does_not_exceed_target():
    """
    O ramp não deve ultrapassar o target_duration_minutes final.
    """
    engine = HabitEngine()
    # Habit com target de 2.1 e baseline de 2.0
    habit = engine.initialize_habit("Meditação", 2.1)
    
    # 2.0 * 1.15 = 2.3 (maior que o target de 2.1)
    new_load = engine.calculate_next_week_load(habit, 0.90)
    
    assert new_load == 2.1
