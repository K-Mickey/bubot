import asyncio

import conf
from bin import loader
from bin.logger import init_logging

if __name__ == '__main__':
    init_logging()
    asyncio.run(loader.run(conf.BOT_TOKEN))
