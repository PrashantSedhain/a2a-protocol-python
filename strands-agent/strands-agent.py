from uuid import uuid4
from strands.models.openai import OpenAIModel
import httpx
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import Message, Part, Role, TextPart
from strands import Agent, tool

from dotenv import load_dotenv
import os

# LOAD ENVIRONMENT VARIABLES
load_dotenv()


@tool
async def call_weather_agent(message: str) -> str:
    """
    Send a message to the A2A agent.

    Args:
        message: The message to send to the agent

    Returns:
        Response from the A2A agent
    """
    try:        
        async with httpx.AsyncClient(timeout=300) as httpx_client:
            resolver = A2ACardResolver(httpx_client=httpx_client, base_url="http://127.0.0.1:9999/")
            agent_card = await resolver.get_agent_card()
            config = ClientConfig(httpx_client=httpx_client, streaming=False)
            factory = ClientFactory(config)
            client = factory.create(agent_card)  

            msg = Message(
                kind="message",
                role=Role.user,
                parts=[Part(TextPart(kind="text", text=message))],
                message_id=uuid4().hex,
            )

            response = client.send_message(msg)

            full_response_text = ""
            async for event in response:
                print(event)
                # 1. Check if the event is a Message object (which contains the text parts)
                if isinstance(event, Message):
                    # 2. Iterate through the list of parts within the Message
                    for part in event.parts:
                        # 3. Check if the root of the Part contains a 'text' attribute
                        #    (A TextPart is often wrapped inside a Part object)
                        if hasattr(part.root, 'text') and part.root.text:
                            # 4. Concatenate the text
                            full_response_text += part.root.text

            return full_response_text

    except Exception as e:
        print(e)
        return f"Error contacting remote weather agent: {str(e)}"

# CREATE MODEL
model = OpenAIModel(
    client_args={
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    model_id="gpt-4o",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)

orchestrator = Agent(
    model=model,
    system_prompt="You are a orchestrator agent and have access to a weather tool that you can call for realtime weather.",
    tools=[call_weather_agent]
)


# RUN AGENT
response = orchestrator("What is the weather in San Francisco?")

# PRINT RESPONSE
print(response)


