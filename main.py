import asyncio

import conf
from bin import loader
from bin.utils import make_dirs, init_logging

if __name__ == "__main__":
    init_logging()
    make_dirs()
    asyncio.run(loader.run(conf.BOT_TOKEN))
    