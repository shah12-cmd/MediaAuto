from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from src.logger import logger
from src.bot import run_fetcher

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(lambda: asyncio.create_task(run_fetcher()), 'interval', minutes=5, id='fetcher')
    scheduler.start()
    logger.info('Scheduler started')

if __name__ == '__main__':
    start_scheduler()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
