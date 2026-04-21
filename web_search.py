import json
import os
import httpx
from dotenv import load_dotenv
from mcp.server import FastMCP

# # 初始化 FastMCP 服务器
app = FastMCP('web-search')
load_dotenv()

API_KEY = os.getenv("TOOL_API_KEY")


def _build_auth_header() -> str:
    if not API_KEY:
        raise ValueError("Missing TOOL_API_KEY in environment")
    return f"Bearer {API_KEY}"

@app.tool()
async def web_search(query: str) -> str:
    """
    搜索互联网内容

    Args:
        query: 要搜索内容

    Returns:
        搜索结果的总结
    """
   
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://open.bigmodel.cn/api/paas/v4/web_search',
            headers={
                "Authorization": _build_auth_header(),
                "Content-Type": "application/json"
            },
            json={
                "search_query": query,
                "search_engine": "search_std",
                "search_intent": False,
                "count": 10,
                "search_domain_filter": "<string>",
                "search_recency_filter": "noLimit",
                "content_size": "medium",
                "request_id": "<string>",
                "user_id": "<string>"
            }
        )

        response = json.loads(response.text)
        
        res_data = []
        for result in response["search_result"]:
            res_data.append(result["content"])

        return '\n\n\n'.join(res_data)
    
if __name__ == "__main__":
    app.run(transport='stdio')
