# -*- coding: utf-8 -*-
import pytest
from neuro_ramp.engine import HabitEngine

def test_auto_deload_5th_week():
    """
    Testa se a cada 5ª semana o load cai 20% (Auto-Deload).
    """
    engine = HabitEngine()
    habit = engine.initialize_habit("Musculação", 60.0)
    
    # Simula 4 semanas completas. A próxima aplicação será para a 5ª semana.
    habit.weeks_completed = 4 
    habit.current_load = 10.0 # Load na semana 4
    
    # Na 5ª semana, independente da aderência, deve ocorrer o deload?
    # O brief diz: "Every 5th week, load drops by 20% to prevent burnout"
    # Geralmente deload é planejado, então vamos assumir que ele acontece 
    # se a aderência foi boa o suficiente para manter o hábito ativo.
    
    new_load, change_type = engine.calculate_next_week_load(habit, 0.90)
    
    # 10.0 * 0.80 = 8.0
    assert new_load == pytest.approx(8.0)
    assert change_type.name == "DELOAD"

def test_normal_ramp_on_4th_week():
    """
    Garante que na 4ª semana (ou outras que não sejam múltiplas de 5) o ramp continue normal.
    """
    engine = HabitEngine()
    habit = engine.initialize_habit("Musculação", 60.0)
    
    habit.weeks_completed = 3 # Próxima é a 4ª
    habit.current_load = 10.0
    
    new_load, change_type = engine.calculate_next_week_load(habit, 0.90)
    
    # 10.0 * 1.15 = 11.5
    assert new_load == pytest.approx(11.5)
    assert change_type.name == "RAMP"

def test_auto_deload_10th_week():
    """
    Verifica se o deload ocorre também na 10ª semana.
    """
    engine = HabitEngine()
    habit = engine.initialize_habit("Musculação", 60.0)
    habit.weeks_completed = 9
    habit.current_load = 20.0
    
    new_load, change_type = engine.calculate_next_week_load(habit, 0.90)
    assert new_load == pytest.approx(16.0) # 20 * 0.8
    assert change_type.name == "DELOAD"

def test_deload_does_not_go_below_baseline():
    """
    Garante que o deload não reduza o hábito para menos que o baseline inicial.
    """
    engine = HabitEngine()
    habit = engine.initialize_habit("Meditação", 10.0) # Baseline 2.0
    
    habit.weeks_completed = 4
    habit.current_load = 2.1 # Próximo de 2.0
    
    # 2.1 * 0.8 = 1.68 (menor que o baseline de 2.0)
    new_load, _ = engine.calculate_next_week_load(habit, 0.90)
    assert new_load == 2.0

def test_recovery_on_week_6():
    """
    Garante que na semana 6 (após o deload) o ramp volte a funcionar normalmente.
    """
    engine = HabitEngine()
    habit = engine.initialize_habit("Musculação", 60.0)
    
    habit.weeks_completed = 5 # Próxima é a 6ª
    habit.current_load = 8.0 # Valor após deload
    
    new_load, change_type = engine.calculate_next_week_load(habit, 0.90)
    assert new_load == pytest.approx(8.0 * 1.15)
    assert change_type.name == "RAMP"
