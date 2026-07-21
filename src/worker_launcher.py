#!/usr/bin/env python3
import asyncio
from src.scheduler import start_scheduler
from src.logger import logger

if __name__ == '__main__':
    start_scheduler()
    logger.info('Worker launching...')
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
