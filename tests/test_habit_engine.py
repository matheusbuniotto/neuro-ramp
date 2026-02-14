from neuro_ramp.engine import HabitEngine
import pytest

def test_habit_initialization_with_baseline():
    """
    Testa se um hábito inicializado segue a regra do baseline (< 2 min).
    """
    engine = HabitEngine()
    habit_name = "Leitura"
    target_duration_minutes = 30
    
    habit = engine.initialize_habit(habit_name, target_duration_minutes)
    
    # O baseline deve ser menor ou igual a 2 minutos
    assert habit.baseline_minutes <= 2
    assert habit.name == habit_name
    assert habit.current_load == habit.baseline_minutes

def test_habit_with_very_small_target():
    """
    Se o alvo já for muito pequeno, o baseline deve ser o próprio alvo ou 2 min.
    """
    engine = HabitEngine()
    habit = engine.initialize_habit("Respiração", 1)
    
    assert habit.baseline_minutes <= 1
    assert habit.current_load == habit.baseline_minutes

def test_apply_next_week_load_increments_counter():
    """
    Verifica se a aplicação do load incrementa o contador de semanas.
    """
    engine = HabitEngine()
    habit = engine.initialize_habit("Coding", 60)
    
    assert habit.weeks_completed == 0
    engine.apply_next_week_load(habit, 0.9)
    assert habit.weeks_completed == 1
    engine.apply_next_week_load(habit, 0.9)
    assert habit.weeks_completed == 2
