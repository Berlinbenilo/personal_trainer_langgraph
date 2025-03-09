from typing import Dict, List, TypedDict


class PersonalWorkoutState(TypedDict):
    age: int
    weight: float
    height: float
    gender: str
    fitness_goal: str
    category: str
    workout_preference: str
    plan_days: int

    equipments: List[str]
    plans: List
    all_workouts: Dict
    workout_type: Dict
    selected_workout_structure: Dict
