import asyncio

import conf
from bin import loader

if __name__ == "__main__":
    asyncio.run(loader.run(conf.BOT_TOKEN))
    