from src.entities.state_model import PersonalWorkoutState
from src.services.agent_service import workout_scheduler_agent, workout_generator_agent, workout_type_chooser_agent
from src.utils.graph_utils import BaseGraph
from langgraph.graph import START, END


async def workout_scheduler(state: PersonalWorkoutState):
    response =await workout_scheduler_agent(state['fitness_goal'], state['category'], state['all_workouts'], state['plans'])
    print(response)
    return response


async def workout_generator(state: PersonalWorkoutState):
    response = await workout_generator_agent(state['equipments'])
    print(response)
    return response


async def workout_type_decider(state: PersonalWorkoutState):
    response = await workout_type_chooser_agent(state['category'], state['plan_days'])
    print(response)
    return response


class PersonalWorkoutGraph(BaseGraph):
    def __init__(self, state):
        super().__init__(state)
        self.agents = [workout_generator, workout_scheduler, workout_type_decider]

        self.add_edges(START, "workout_generator")
        self.add_edges(START, "workout_type_decider")
        self.add_edges("workout_generator", "workout_scheduler")
        self.add_edges("workout_type_decider", "workout_scheduler")
        self.add_edges("workout_scheduler", END)

