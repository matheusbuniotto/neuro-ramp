# -*- coding: utf-8 -*-
import pytest
from datetime import time
from neuro_ramp.engine import HabitEngine

def test_morning_multiplier_active():
    """
    Verifica se o multiplicador de 2.3x é aplicado entre 6:00 e 8:00.
    """
    engine = HabitEngine()
    
    # 7:00 AM está dentro do pico de cortisol (6-8 AM)
    completion_time = time(7, 0)
    multiplier = engine.get_completion_multiplier(completion_time)
    
    assert multiplier == 2.3

def test_morning_multiplier_inactive_early():
    """
    Verifica se antes das 6:00 o multiplicador é 1.0.
    """
    engine = HabitEngine()
    
    # 5:59 AM está fora do pico
    completion_time = time(5, 59)
    multiplier = engine.get_completion_multiplier(completion_time)
    
    assert multiplier == 1.0

def test_morning_multiplier_inactive_late():
    """
    Verifica se após as 8:00 o multiplicador é 1.0.
    """
    engine = HabitEngine()
    
    # 8:01 AM está fora do pico
    completion_time = time(8, 1)
    multiplier = engine.get_completion_multiplier(completion_time)
    
    assert multiplier == 1.0

def test_multiplier_at_boundaries():
    """
    Verifica as fronteiras exatas (6:00 e 8:00).
    """
    engine = HabitEngine()
    
    assert engine.get_completion_multiplier(time(6, 0)) == 2.3
    assert engine.get_completion_multiplier(time(8, 0)) == 2.3

def test_habit_score_with_multiplier():
    """
    Verifica se o score final reflete o multiplicador.
    Score = load * multiplier
    """
    engine = HabitEngine()
    habit = engine.initialize_habit("Leitura", 30) # load 2.0
    
    # 7:00 AM -> 2.3x
    completion_time = time(7, 0)
    score = engine.calculate_completion_score(habit, completion_time)
    
    # 2.0 * 2.3 = 4.6
    assert score == pytest.approx(4.6)

def test_habit_score_without_multiplier():
    """
    Verifica score sem multiplicador (1.0x).
    """
    engine = HabitEngine()
    habit = engine.initialize_habit("Leitura", 30) # load 2.0
    
    # 10:00 AM -> 1.0x
    completion_time = time(10, 0)
    score = engine.calculate_completion_score(habit, completion_time)
    
    assert score == 2.0
