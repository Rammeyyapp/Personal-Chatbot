# 🤖 Personal AI Agent: Autonomous Assistant with API Orchestration

This project implements a fully **local, privacy-preserving AI Agent** that serves as a personal assistant capable of executing real-world, multi-domain tasks. It is built entirely on open-source components, demonstrating a robust architecture for Agentic AI workflows without relying on paid cloud services for core intelligence.

---

## 🎯 Core Function and Architecture

The system's core function is to intelligently orchestrate external API tools based on a natural language user request, following a streamlined **Think-Plan-Act** loop. A unique dual-LLM approach is used to optimize efficiency and resource utilization.

### Component Breakdown

| Layer | Component | Role in Agent Loop | Description & Purpose |
| :--- | :--- | :--- | :--- |
| **Agent's Brain** | `llama3.1` (via Ollama) | Advanced Planning | Used for complex reasoning and generating the structured **tool-call JSON** payload. |
| **Intent Classifier** | `phi3:mini` (via Ollama) | Initial/Fast Thinking | Used for quick classification of user query as `TOOL_CALL` or `CONVERSATION`. |
| **Orchestration** | LangChain / LangGraph | Logic Layer | Handles the ReAct loop, tool definition, and overall agent execution flow. |
| **API Server** | FastAPI / Python | Action & Gateway | Receives the user request, executes the agent logic, and handles the actual API calls (e.g., sending an email, querying a database) based on the LLM's plan. |

---

## 🚀 Key Use Cases and Capabilities

The agent's value lies in automating repetitive or multi-step tasks that traditionally require manual switching between applications, all while ensuring user data remains private.

1.  **Workflow Automation & API Orchestration:** The agent translates high-level requests into structured actions across different domains.
    * *Example:* Translating *"Send an email to John about the project update with no subject"* into a structured $\text{send\_email(recipient, subject, body)}$ call.
2.  **Personal Productivity & Information Retrieval:** It acts as a digital co-pilot for daily tasks.
    * *Example:* Automating travel lookups using $\text{search\_trains(source\_city, destination\_city, date\_of\_journey)}$.
3.  **Technical Differentiator: Privacy and Cost-Efficiency:**
    * All natural language processing, planning, and intent classification occur **locally** via Ollama, ensuring data never leaves the device and eliminating reliance on paid, rate-limited cloud APIs for the core intelligence.

---

## 🏗️ Technology Stack

The agent is built on a modern, open-source stack designed for speed, flexibility, and local operation.

| Layer | Component | Description & Purpose |
| :--- | :--- | :--- |
| **LLM Engine** | **Ollama** | Core service for running open-source LLMs ($\text{llama3.1}$, $\text{phi3:mini}$) directly on the local machine. |
| **Backend/Orchestration** | **Python, LangChain, FastAPI** | Primary language for logic. LangChain handles the agent logic, and FastAPI serves as the high-speed API gateway. |
| **Data Validation** | **Pydantic** | Used for data validation and structured output, ensuring clean, type-safe data exchange for tool-calling payloads. |
| **Frontend/UI** | **React / Next.js** | A modern JavaScript framework for building the dynamic, interactive chat interface, styled with **Tailwind CSS**. |

---

## 🛠️ Environment Setup

The environment is divided into the Local LLM Server (Ollama) and the Application Stack (FastAPI & React).

### 1. Local LLM Server (Ollama)

1.  **Install Ollama:** Download and install the application for your OS (macOS, Windows, Linux).
2.  **Pull Models:** Use the command line to download the necessary models:
    ```bash
    ollama pull llama3
    ollama pull phi3:mini
    ```
3.  **Run Server:** Ollama automatically runs in the background, exposing its API on the default port ($\text{http://localhost:11434}$).

### 2. Application Stack (FastAPI & React)

| Component | Prerequisites | Setup Commands / Configuration |
| :--- | :--- | :--- |
| **Backend** | Python (3.10+), pip | `pip install fastapi uvicorn python-multipart langchain ollama`<br>Run: `uvicorn main:app --reload` |
| **Frontend** | Node.js (v18+), npm/yarn | `npx create-next-app@latest my-agent-ui`<br>`npm install tailwindcss`<br>Run: `npm run dev` |
| **Integration** | Environment Variables | Configure the FastAPI service to point to the local LLM endpoint: `OLLAMA_BASE_URL=http://localhost:11434` |

---

## ☁️ Hosting and Deployment

The solution is structured to maximize flexibility while preserving the core privacy features.

* **Frontend Deployment (Netlify):** The **React/Next.js frontend** is deployed to **Netlify** for its speed, global CDN, and streamlined CI/CD pipeline. The UI communicates with the external API Gateway.
* **Backend & Intelligence (External):** The **FastAPI server** and the **Ollama LLM Engine** run on separate infrastructure. Crucially, the **Ollama LLM Server** runs on the user's local machine to maintain the **privacy-preserving** guarantee, while the FastAPI server acts as a proxy/gateway between the public UI and the local core.

---

## 🖼️ Conceptual Architecture (Wireframe)

The system employs a sequential request flow based on the $\text{ReAct}$ pattern:

1.  **User Input:** The **React UI** captures the user's message.
2.  **API Call:** The UI sends a $\text{POST}$ request with the message to the **FastAPI Server** ($\text{/api/chat}$).
3.  **Agent Invocation:** The FastAPI server passes the message to the **LangChain Agent** logic.
4.  **LLM Decision:** The agent sends the message and tool schemas to **Ollama** (via its API).
5.  **Execution:** If a tool is needed, the agent executes the action via the **FastAPI Server**'s underlying Python logic and gets an **Observation**.
6.  **Final Response:** The LangChain Agent formats the final, natural language answer and sends it back to the **FastAPI Server**.
7.  **Display:** The FastAPI server returns the JSON response to the React UI, displaying the final output to the user.
