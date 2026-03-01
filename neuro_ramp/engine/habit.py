# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import time

class ChangeType(Enum):
    RAMP = auto()
    DELOAD = auto()
    MAINTAIN = auto()

@dataclass
class Habit:
    name: str
    target_duration_minutes: float
    # current_load representa o volume atual do hábito para o usuário
    current_load: float = field(init=False)
    # baseline_minutes é o valor inicial do hábito, garantindo <= 2 min
    baseline_minutes: float = field(init=False)
    # Contador de semanas e dias para lógica de ramp, deload e automaticidade
    weeks_completed: int = 0
    days_completed: int = 0
    # Rastreia a última mudança para feedback na UI
    last_change: ChangeType = ChangeType.MAINTAIN

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

    def calculate_next_week_load(self, habit: Habit, adherence_rate: float) -> tuple[float, ChangeType]:
        """
        Calcula o load para a próxima semana e o tipo de mudança.
        - A cada 5 semanas, ocorre um Auto-Deload (-20%).
        - Caso contrário, se a aderência for > 80%, aumenta em 15% (Ramp).
        O valor nunca deve ultrapassar o target_duration_minutes.
        """
        # Verificamos se a PRÓXIMA semana é a 5ª (múltiplo de 5)
        next_week_number = habit.weeks_completed + 1
        
        if next_week_number % 5 == 0:
            # Auto-Deload: Redução de 20%
            new_load = habit.current_load * 0.80
            final_load = round(max(habit.baseline_minutes, new_load), 2)
            return final_load, ChangeType.DELOAD

        if adherence_rate > 0.8:
            new_load = habit.current_load * 1.15
            # Cap no target e arredonda para 2 casas decimais para clareza na UI
            final_load = round(min(new_load, habit.target_duration_minutes), 2)
            
            if final_load > habit.current_load:
                return final_load, ChangeType.RAMP
        
        return habit.current_load, ChangeType.MAINTAIN

    def apply_next_week_load(self, habit: Habit, adherence_rate: float) -> None:
        """
        Calcula e aplica o novo load diretamente no objeto Habit, 
        e incrementa o contador de semanas.
        """
        new_load, change_type = self.calculate_next_week_load(habit, adherence_rate)
        habit.current_load = new_load
        habit.weeks_completed += 1
        habit.last_change = change_type

    def get_completion_multiplier(self, completion_time: time) -> float:
        """
        Retorna o multiplicador de progresso baseado no horário de conclusão.
        Pico de cortisol (06:00 - 08:00) garante 2.3x.
        """
        start_peak = time(6, 0)
        end_peak = time(8, 0)
        
        if start_peak <= completion_time <= end_peak:
            return 2.3
        
        return 1.0

    def calculate_completion_score(self, habit: Habit, completion_time: time) -> float:
        """
        Calcula o score de conclusão baseado no load atual e no multiplicador de horário.
        """
        multiplier = self.get_completion_multiplier(completion_time)
        return round(habit.current_load * multiplier, 2)
