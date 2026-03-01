# -*- coding: utf-8 -*-
from datetime import datetime
from fastapi import FastAPI
from neuro_ramp.engine import HabitEngine
from neuro_ramp.ui.presenter import UIPresenter
from neuro_ramp.ui.schemas import FocusScreenState

app = FastAPI(title="NEURO-RAMP API")
engine = HabitEngine()
presenter = UIPresenter(engine)

# Mock de hábito para demonstração no Focus Screen
demo_habit = engine.initialize_habit("Kettlebell Swings", 50)
demo_habit.weeks_completed = 2

@app.get("/focus", response_model=FocusScreenState)
async def get_focus_screen():
    """
    Retorna o estado da tela de foco para o hábito atual.
    """
    current_time = datetime.now().time()
    return presenter.get_focus_state(demo_habit, current_time)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
