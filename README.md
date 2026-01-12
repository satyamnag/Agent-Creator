# 🤖 Agent Creator

#### Agent Creator is an autonomous AI system that generates, registers, and launches new AI agents at runtime using Autogen Core and Autogen AgentChat.
#### Each created agent becomes a fully independent Python module with its own logic, personality, and system prompt.

## ✨ Key Features

### 🧠 Autonomous Agent Generation
#### The Creator Agent reads a predefined Python template and automatically builds new agent classes on demand.

### 📦 Dynamic Module Creation
#### New agents are saved as individual Python files inside "/agents/{agent_name}.py", making them modular, reusable, and instantly importable.

### ⚡ Live Runtime Registration
#### Every generated agent is automatically registered and activated within AutoGen—no manual setup needed.

### 🎯 Template-Based Consistency
#### All agents follow a consistent class structure and shared inheritance pattern, ensuring uniform behavior and maintainability.

### 💡 Autonomous Development Cycle
#### Once an agent is created, it immediately begins operating independently, generating outputs or tasks without manual intervention and stores it under "ideas/{idea_name}.md".

## 🔐 Environment Variables
#### OPENAI_API_KEY=your openai api key
