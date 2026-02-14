# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

@dataclass
class Habit:
    name: str
    target_duration_minutes: float
    # current_load representa o volume atual do hábito para o usuário
    current_load: float = field(init=False)
    # baseline_minutes é o valor inicial do hábito, garantindo <= 2 min
    baseline_minutes: float = field(init=False)

    def __post_init__(self):
        # A regra do baseline: <= 2 minutos.
        # Se o target_duration_minutes já for menor ou igual a 2, o baseline é o próprio target (com um mínimo de 0.1).
        # Caso contrário, o baseline é 2 minutos.
        if self.target_duration_minutes <= 2.0:
            self.baseline_minutes = max(0.1, self.target_duration_minutes)
        else:
            self.baseline_minutes = 2.0
        
        # O load inicial é sempre o baseline
        self.current_load = self.baseline_minutes

class HabitEngine:
    def initialize_habit(self, name: str, target_duration_minutes: float) -> Habit:
        """
        Inicializa um novo hábito com base no nome e duração alvo, aplicando a regra do baseline.
        """
        return Habit(name=name, target_duration_minutes=target_duration_minutes)

    def calculate_next_week_load(self, habit: Habit, adherence_rate: float) -> float:
        """
        Calcula o load para a próxima semana.
        Se a aderência for > 80%, aumenta em 15%.
        O valor nunca deve ultrapassar o target_duration_minutes.
        """
        if adherence_rate > 0.8:
            new_load = habit.current_load * 1.15
            # Cap no target
            return min(new_load, habit.target_duration_minutes)
        
        return habit.current_load
