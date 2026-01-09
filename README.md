# 🤖 Agent Creator

### Agent Creator is an autonomous system that dynamically generates, registers, and launches new AI agents at runtime using Autogen Core and Autogen AgentChat.
### Each generated agent is a fully independent Python module with its own logic, personality, and system message.

## ✨ Key Features

## 🧠 Autonomous Agent Generation
### Creator reads a Python template and generates a new agent class automatically.

## 📦 Dynamic Module Creation
### Saves source files into /agents/<name>.py and imports them at runtime.

## ⚡ Live Runtime Registration
### Each generated agent is instantly registered and activated within Autogen.

## 🛡️ UTF-8 Safe Across Platforms
### Includes guards to prevent Windows & Unicode encoding crashes.

## 🎯 Template-Based Consistency
### All agents maintain the same class structure and inheritance.

## 💡 Automatic First Task
### Creator immediately prompts new agents to generate their first idea.
