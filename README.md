# A2A Protocol Python - Agent-to-Agent Communication

A comprehensive demonstration of the **Agent-to-Agent (A2A) Protocol** implemented in Python, showcasing how to build distributed AI agents that can communicate and collaborate with each other using the A2A SDK.

## Overview

This project demonstrates two different approaches to building A2A-compliant agents:

1. **OpenAI Agent** - A weather agent built using the OpenAI agents framework that exposes an A2A interface
2. **Strands Agent** - An orchestrator agent built using Strands that calls remote A2A agents as tools

## Project Structure

```
a2a-protocol-python/
├── openai-agent/
│   ├── __main__.py          # Weather agent server implementation
│   └── requirements.txt      # Python dependencies
├── strands-agent/
│   ├── strands-agent.py      # Orchestrator agent that calls remote agents
│   └── requirements.txt      # Python dependencies
└── README.md                 # This file
```

## What is A2A Protocol?

The Agent-to-Agent (A2A) Protocol is a standard for enabling autonomous agents to discover, understand, and communicate with other agents in a distributed network. It provides:

- **Agent Discovery**: Find available agents and their capabilities
- **Standardized Communication**: Exchange messages using a common format
- **Tool Integration**: Agents can expose their functionality as tools for other agents
- **Scalability**: Build complex AI systems by composing multiple specialized agents

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- OpenAI API key (for the orchestrator example)

### Installation & Running

#### 1. Start the OpenAI Weather Agent Server

```bash
cd openai-agent
pip install -r requirements.txt
python -m _main__
```

The agent server will start on `http://localhost:9999/`

#### 2. Run the Strands Orchestrator Agent

In a new terminal:

```bash
cd strands-agent
pip install -r requirements.txt
export OPENAI_API_KEY=your_api_key_here
python strands-agent.py
```

The orchestrator will send a query to the weather agent and print the response.

## How It Works

### OpenAI Agent (Provider)

The OpenAI agent implements:
- A `WeatherAgent` class with a `get_weather` tool
- An `RemoteWeatherAgentExecutor` that handles A2A requests
- An A2A-compliant HTTP server using Starlette
- Publishes an `AgentCard` describing its capabilities

```python
# Example: Get weather in a city
WeatherAgent.get_weather("Seattle") → "Current weather in Seattle is 80 Fahrenheit and sunny."
```

### Strands Agent (Consumer)

The Strands agent implements:
- An orchestrator that uses OpenAI's GPT-4o model
- A `call_weather_agent` tool that communicates with remote A2A agents
- Uses the A2A SDK to discover and call the weather agent
- Handles streaming responses from remote agents

```
User Query
    ↓
Strands Orchestrator (GPT-4o)
    ↓
Decides to use weather tool
    ↓
A2A Client (discovers & calls remote agent)
    ↓
OpenAI Weather Agent
    ↓
Returns weather information
    ↓
Orchestrator formats final response
```

## API Examples

### Querying the Weather Agent

**Direct Agent Call:**
```python
weather_agent = WeatherAgent()
response = await weather_agent.invoke("What is the temperature in Seattle?")
```

**Via A2A Protocol:**
```bash
curl -X POST http://localhost:9999/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the temperature in Seattle?"}'
```

### Agent Card

The weather agent publishes its capabilities via an `AgentCard`:

```python
AgentCard(
    name='Weather Agent',
    description='Just a weather agent',
    url='http://localhost:9999/',
    version='1.0.0',
    default_input_modes=['text'],
    default_output_modes=['text'],
    capabilities=AgentCapabilities(streaming=False),
    skills=[
        AgentSkill(
            id='Weather Agent',
            name='Returns the weather in a given city',
            description='Provides weather information.',
            tags=['weather'],
            examples=['what is the weather in San Francisco?'],
        )
    ],
)
```

## Key Concepts

### Agent Skills

Agents expose their capabilities as `AgentSkill` objects that describe:
- What the agent can do
- How to use it (examples)
- Input/output modes (text, streaming, etc.)

### Agent Card

The `AgentCard` is like a resume for an agent. It tells other agents:
- The agent's name and description
- Where to find it (URL)
- What version it is
- What skills it offers
- What communication modes it supports

### A2A SDK Components

- **A2ACardResolver**: Discovers and fetches agent cards from A2A servers
- **ClientFactory**: Creates clients to communicate with discovered agents
- **EventQueue**: Handles asynchronous event processing
- **AgentExecutor**: Base class for implementing A2A-compliant agent handlers

## Dependencies

### OpenAI Agent
- `openai-agents`: Framework for building agents with OpenAI models
- `a2a-sdk`: A2A protocol implementation
- `uvicorn`: ASGI server for running the HTTP endpoint
- `starlette`: Web framework for handling A2A requests

### Strands Agent
- `strands-agents`: Framework for building orchestrator agents
- `strands-agents-tools`: Tools integration for Strands agents
- `a2a-sdk`: A2A client libraries and type definitions
- `python-dotenv`: Environment variable management
- `httpx`: Async HTTP client for communicating with agents

## Use Cases

- **Multi-agent Systems**: Build complex workflows by connecting specialized agents
- **Agent Networks**: Create a network of agents that can discover and collaborate
- **Distributed AI**: Scale AI capabilities across multiple servers and services
- **AI Orchestration**: Coordinate multiple AI services to solve complex problems
- **Tool Sharing**: Expose agent capabilities as reusable tools for other agents

## Learning Resources

This project is part of the "AI With Prashant - A2A Crash Course" and demonstrates practical implementation of the A2A protocol. Explore the code to understand:

1. How to build A2A-compliant agents
2. How agents discover each other
3. How agents communicate and share capabilities
4. How to orchestrate multiple agents for complex tasks

## Next Steps

- Modify the weather agent to return real weather data
- Add more tools to the weather agent
- Create additional specialized agents (stocks, news, etc.)
- Build more complex orchestrator queries
- Deploy agents to cloud platforms

## License

This project is for educational purposes.

## Resources

- [A2A SDK Documentation](https://github.com/a2a-protocol)
- [OpenAI Agents Framework](https://github.com/openai/agents)
- [Strands Agents](https://github.com/modelcontextprotocol)
