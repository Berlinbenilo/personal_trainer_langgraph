import asyncio
from pprint import pprint

from langgraph.checkpoint.memory import MemorySaver

from src.services.graph_service import PersonalWorkoutGraph, PersonalWorkoutState

memory = MemorySaver()


async def main():
    personal_workout = PersonalWorkoutGraph(PersonalWorkoutState)
    output = await personal_workout.run(memory=memory, input_payload={"category": "beginner", "fitness_goal": "weight gain",
                                                                      "equipments": [
                                                                          'dumbbell'], "plan_days": 7, "plans":[]},
                                        config={"configurable": {"thread_id": "6367"}})
    return output


if __name__ == '__main__':
    response = asyncio.run(main())
    pprint(response)
