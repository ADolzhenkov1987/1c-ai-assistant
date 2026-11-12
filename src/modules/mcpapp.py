# src/modules/mcpapp.py
from mcp.server.mcpserver import MCPServer  # SDK 2.x; для mcp<2 было: from mcp.server.fastmcp import FastMCP

from main import main


mcp = MCPServer("1c-ai-assistant")


@mcp.tool()
async def ask_1c_assistant(question: str, user_id: str) -> str:
    """Отвечает на вопросы по разработке 1С.

    Args:
        question: текст вопроса по разработке 1С
        user_id: идентификатор пользователя для хранения истории диалога
    """
    return await main(question, user_id)
