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
    
    new_load = engine.calculate_next_week_load(habit, 0.90)
    
    # 10.0 * 0.80 = 8.0
    assert new_load == pytest.approx(8.0)

def test_normal_ramp_on_4th_week():
    """
    Garante que na 4ª semana (ou outras que não sejam múltiplas de 5) o ramp continue normal.
    """
    engine = HabitEngine()
    habit = engine.initialize_habit("Musculação", 60.0)
    
    habit.weeks_completed = 3 # Próxima é a 4ª
    habit.current_load = 10.0
    
    new_load = engine.calculate_next_week_load(habit, 0.90)
    
    # 10.0 * 1.15 = 11.5
    assert new_load == pytest.approx(11.5)
