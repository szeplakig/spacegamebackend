from arq import ArqRedis, create_pool
from arq.connections import RedisSettings


async def get_redis() -> ArqRedis:
    return await create_pool(RedisSettings())
