from typing import Dict, Any, List, Optional
from anthropic import Anthropic
from datetime import datetime
from loguru import logger
import os
from agents.tools import AgentTools, AVAILABLE_TOOLS

class BaseAgent:
    """Clase base para todos los agentes con soporte para Tool Use"""

    def __init__(
        self,
        name: str,
        role: str,
        department: str,
        system_prompt: str,
        model: str = "claude-sonnet-4",
        tools: List[str] = None,
        manager = None  # WebSocket manager para broadcasts
    ):
        self.name = name
        self.role = role
        self.department = department
        self.system_prompt = system_prompt
        self.model = model
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.status = "offline"
        self.current_activity = None
        self.tool_handler = AgentTools()
        self.manager = manager  # Guardar manager

        # Filtrar herramientas disponibles para este agente
        if tools:
            self.available_tools = [t for t in AVAILABLE_TOOLS if t["name"] in tools]
        else:
            self.available_tools = []

    async def _broadcast(self, message_type: str, activity: str = None):
        """Enviar actualización por WebSocket"""
        if self.manager:
            try:
                await self.manager.broadcast({
                    "type": message_type,
                    "agent_name": self.name,
                    "role": self.role,
                    "department": self.department,
                    "status": self.status,
                    "activity": activity or self.current_activity,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as e:
                logger.error(f"Error broadcasting: {e}")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar una tarea (con soporte para Tool Use)"""
        try:
            self.status = "working"
            self.current_activity = task.get("description", "Procesando tarea")

            logger.info(f"[{self.name}] Iniciando tarea: {task.get('title')}")

            # Broadcast: inicio de trabajo
            await self._broadcast("agent_status", f"Iniciando: {task.get('title', 'tarea')}")

            # Preparar el prompt
            user_message = self._prepare_prompt(task)

            # Ejecutar con tool use si el agente tiene herramientas
            if self.available_tools:
                output = await self._execute_with_tools(user_message)
            else:
                output = await self._execute_simple(user_message)

            result = {
                "agent": self.name,
                "task_id": task.get("id"),
                "status": "completed",
                "output": output,
                "completed_at": datetime.utcnow().isoformat()
            }

            logger.info(f"[{self.name}] Tarea completada")
            self.status = "online"

            # Broadcast: tarea completada
            await self._broadcast("agent_status", "✅ Tarea completada")
            self.current_activity = "Esperando nueva tarea"

            return result

        except Exception as e:
            logger.error(f"[{self.name}] Error en tarea: {str(e)}")
            self.status = "error"
            return {
                "agent": self.name,
                "task_id": task.get("id"),
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.utcnow().isoformat()
            }

    async def _execute_simple(self, user_message: str) -> str:
        """Ejecutar sin herramientas"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=self.system_prompt,
            messages=[{
                "role": "user",
                "content": user_message
            }]
        )

        return response.content[0].text

    async def _execute_with_tools(self, user_message: str) -> str:
        """Ejecutar con Tool Use (agentic loop)"""
        messages = [{
            "role": "user",
            "content": user_message
        }]

        # Loop agentic: Claude puede usar herramientas múltiples veces
        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            logger.info(f"[{self.name}] Tool use iteration {iteration}")

            # Llamar a Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.system_prompt,
                messages=messages,
                tools=self.available_tools
            )

            # Si no hay más tool_use, terminamos
            if response.stop_reason == "end_turn":
                # Extraer texto final
                final_text = ""
                for content in response.content:
                    if content.type == "text":
                        final_text += content.text
                return final_text

            # Procesar tool_use
            if response.stop_reason == "tool_use":
                # Agregar respuesta de Claude a mensajes
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })

                # Ejecutar herramientas y recopilar resultados
                tool_results = []

                for content in response.content:
                    if content.type == "tool_use":
                        tool_name = content.name
                        tool_input = content.input

                        logger.info(f"[{self.name}] Usando herramienta: {tool_name}")

                        # Ejecutar la herramienta
                        result = await self._execute_tool(tool_name, tool_input)

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": str(result)
                        })

                # Agregar resultados de herramientas a mensajes
                messages.append({
                    "role": "user",
                    "content": tool_results
                })

                # Continuar el loop
                continue

            # Si llegamos aquí, algo salió mal
            break

        # Si salimos del loop sin respuesta final
        return "Error: Máximo de iteraciones alcanzado"

    async def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """Ejecutar una herramienta específica"""
        try:
            if tool_name == "get_company_config":
                return self.tool_handler.get_company_config()

            elif tool_name == "web_search":
                return await self.tool_handler.web_search(
                    query=tool_input.get("query"),
                    num_results=tool_input.get("num_results", 5)
                )

            elif tool_name == "analyze_social_media":
                return await self.tool_handler.analyze_social_media_account(
                    platform=tool_input.get("platform"),
                    username=tool_input.get("username")
                )

            elif tool_name == "analyze_competitor_website":
                return await self.tool_handler.analyze_competitor_website(
                    url=tool_input.get("url")
                )

            elif tool_name == "get_industry_trends":
                return await self.tool_handler.get_industry_trends(
                    industry=tool_input.get("industry"),
                    timeframe=tool_input.get("timeframe", "30d")
                )

            else:
                return {"error": f"Herramienta desconocida: {tool_name}"}

        except Exception as e:
            logger.error(f"Error ejecutando {tool_name}: {str(e)}")
            return {"error": str(e)}

    def _prepare_prompt(self, task: Dict[str, Any]) -> str:
        """Preparar el prompt para Claude"""
        prompt = f"# Tarea: {task.get('title')}\n\n"

        if task.get('description'):
            prompt += f"## Descripción:\n{task['description']}\n\n"

        if task.get('input_data'):
            prompt += f"## Datos de entrada:\n{task['input_data']}\n\n"

        if task.get('context'):
            prompt += f"## Contexto:\n{task['context']}\n\n"

        prompt += "Por favor, completa esta tarea según tu rol y responsabilidades."

        # Si tiene herramientas, mencionar que puede usarlas
        if self.available_tools:
            tool_names = [t["name"] for t in self.available_tools]
            prompt += f"\n\nTienes acceso a estas herramientas: {', '.join(tool_names)}"
            prompt += "\nUsa las herramientas cuando necesites información actualizada o datos externos."

        return prompt

    def get_status(self) -> Dict[str, Any]:
        """Obtener estado actual del agente"""
        return {
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "status": self.status,
            "current_activity": self.current_activity,
            "tools_available": len(self.available_tools)
        }
