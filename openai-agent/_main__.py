import uvicorn
import asyncio
from a2a.server.apps import A2AStarletteApplication
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from a2a.utils import (
    new_agent_text_message
)

from agents import Agent, Runner, function_tool
from a2a.server.agent_execution import AgentExecutor, RequestContext

# Test the agent only
async def main():
    weather_agent = WeatherAgent()
    # Await the call within the async function
    response = await weather_agent.invoke("What is the temperature in Seattle?")
    print(response)

# The entry point for a standard async script
if __name__ == "__main__":
    asyncio.run(main())


class WeatherAgent:

    @function_tool
    def get_weather(city: str):
        return f"Current weather in {city} is 80 Fahrenheit and sunny."


    def __init__(self):
        self.agent = Agent(
            name="WeatherAgent",
            instructions="You are a helpful assistant that returns weather information using the available tool.",
            tools=[self.get_weather],
        )

    async def invoke(self, query: str) -> str:
        try:
            result = await Runner.run(self.agent, query)
            return result.final_output
        except Exception as e:
            print("An error occured", e)


class RemoteWeatherAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = WeatherAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        user_input = context.get_user_input()
        # task = context.current_task
        # context_id = context.context_id

        try:
            result = await self.agent.invoke(user_input)
            await event_queue.enqueue_event(new_agent_text_message(result))

        except Exception as e:
            await event_queue.enqueue_event(new_agent_text_message(f"Error: {str(e)}"))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not implemented")

if __name__ == '__main__':
    # --8<-- [start:AgentSkill]
    skill = AgentSkill(
        id='Weather Agent',
        name='Returns the weather in a given city',
        description='Provides weather information.',
        tags=['weather'],
        examples=['what is the weather in San Francisco?'],
    )


    public_agent_card = AgentCard(
        name='Weather Agent',
        description='Just a weather agent',
        url='http://localhost:9999/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
        supports_authenticated_extended_card=True,
    )

    request_handler = DefaultRequestHandler(
        agent_executor=RemoteWeatherAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=public_agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host='0.0.0.0', port=9999)
