from typing import List

from src.constants.general_properties import model_config, model_provider, workout_types
from src.constants.prompt_properties import equipment_exercise_prompt, schedular_prompt, workout_type_prompt
from src.entities.validator_model import AllWorkouts, Schedular, WorkoutType
from src.utils.llm_utils import LLMWrapper

llm = LLMWrapper(model_config=model_config, model_provider=model_provider)


async def workout_scheduler_agent(fitness_goal, category, all_workouts, plans):

    workouts = ""
    for all_workout in all_workouts:
        workouts += f"""For {all_workout['equipment_name']} workout. The workouts are \n
                {"".join([f"{i + 1}. {workout} \n" for i, workout in enumerate(all_workout['Workouts'])])}"""
    payload = {
        "fitness_goal": fitness_goal,
        "user_experience": category,
        "workouts": workouts,
        "plan": "".join([f"For day {plan['day_no']}, the workout type is {plan['workout_type']} \n" for plan in plans])
    }
    llm_response = await llm.invoke_with_parser(prompt=schedular_prompt, placeholder_input=payload,
                                                output_validator=Schedular)
    return llm_response


async def workout_generator_agent(equipments: List[str]):
    payload = {
        "equipments": equipments,
    }
    llm_response = await llm.invoke_with_parser(prompt=equipment_exercise_prompt, placeholder_input=payload,
                                                output_validator=AllWorkouts)
    return llm_response


async def workout_type_chooser_agent(category, plan_days):
    payload = {
        "workout_types": workout_types,
        "category": category,
        "number_of_days": plan_days
    }
    llm_response = await llm.invoke_with_parser(prompt=workout_type_prompt, placeholder_input=payload,
                                                output_validator=WorkoutType)
    return {"workout_type": llm_response}
