import asyncio
import json

from src.stage1.discord_tools import create_thread
from discord_client.models import CreateForumThreadRequest, BaseCreateMessageCreateRequest


async def test():
    thread_result = await create_thread(channel_id="1191354485679857837", thread=CreateForumThreadRequest(name="Testthread", message=BaseCreateMessageCreateRequest(content="this is a test")))
    # Convert the thread result to JSON for printing
    print(json.dumps(thread_result.to_dict(), indent=2))

asyncio.run(test())
