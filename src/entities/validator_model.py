from typing import List

from pydantic import BaseModel, Field


class WorkoutScheme(BaseModel):
    number_of_set: int = Field(description="Number of sets")
    number_of_reps: str = Field(description="Range of reps in each set")
    workout_name: str = Field(description="Name of the workout")
    rest_time: str = Field(description="rest time between each set")


class EnduranceTraining(BaseModel):
    cardiovascular: List[WorkoutScheme]
    muscular_endurance: List[WorkoutScheme]


class Workouts(BaseModel):
    equipment_name: str = Field(description="Name of the workout equipment")
    Workouts: List[str] = Field(description="List of workout names that performed by an workout equipment")


class AllWorkouts(BaseModel):
    all_workouts : List[Workouts]


class WorkoutType(BaseModel):
    day_no: int = Field(description="Day number")
    workout_type: List[str] = Field(description="Chosen workout type for the corresponding day")


class DaySchedule(BaseModel):
    day_no: int = Field(description="Day number")
    workouts: List[EnduranceTraining]


class Schedular(BaseModel):
    selected_workout_structure: List[DaySchedule]
