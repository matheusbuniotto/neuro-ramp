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
    # Contador de semanas para lógica de ramp e deload
    weeks_completed: int = 0

    def __post_init__(self):
        # Regra do baseline: Inicia com no máximo 2 minutos.
        # Se o target for menor que 2 minutos, o baseline é o target.
        # Se o target for maior que 2 minutos, o baseline é 2 minutos.
        # Mantemos um mínimo de 0.1 minutos para visibilidade, a menos que o target seja menor.
        
        limit = 2.0
        self.baseline_minutes = min(self.target_duration_minutes, limit)
        
        # Garantir que não seja 0 se o target for > 0
        if self.target_duration_minutes > 0:
            self.baseline_minutes = max(min(0.1, self.target_duration_minutes), self.baseline_minutes)

        # O load inicial é sempre o baseline
        self.current_load = round(self.baseline_minutes, 2)

class HabitEngine:
    def initialize_habit(self, name: str, target_duration_minutes: float) -> Habit:
        """
        Inicializa um novo hábito com base no nome e duração alvo, aplicando a regra do baseline.
        """
        return Habit(name=name, target_duration_minutes=target_duration_minutes)

    def calculate_next_week_load(self, habit: Habit, adherence_rate: float) -> float:
        """
        Calcula o load para a próxima semana.
        - A cada 5 semanas, ocorre um Auto-Deload (-20%).
        - Caso contrário, se a aderência for > 80%, aumenta em 15% (Ramp).
        O valor nunca deve ultrapassar o target_duration_minutes.
        """
        # Verificamos se a PRÓXIMA semana é a 5ª (múltiplo de 5)
        next_week_number = habit.weeks_completed + 1
        
        if next_week_number % 5 == 0:
            # Auto-Deload: Redução de 20%
            new_load = habit.current_load * 0.80
            return round(max(habit.baseline_minutes, new_load), 2)

        if adherence_rate > 0.8:
            new_load = habit.current_load * 1.15
            # Cap no target e arredonda para 2 casas decimais para clareza na UI
            return round(min(new_load, habit.target_duration_minutes), 2)
        
        return habit.current_load

    def apply_next_week_load(self, habit: Habit, adherence_rate: float) -> None:
        """
        Calcula e aplica o novo load diretamente no objeto Habit, 
        e incrementa o contador de semanas.
        """
        habit.current_load = self.calculate_next_week_load(habit, adherence_rate)
        habit.weeks_completed += 1
