"""Message scheduling and automation"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Callable
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)


class MessageScheduler:
    """Schedule and manage message sending"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.send_task: Optional[Callable] = None
    
    def start(self) -> None:
        """Start scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")
    
    def stop(self) -> None:
        """Stop scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
    
    def schedule_periodic_task(self, func: Callable, interval_seconds: int,
                               job_id: str = "periodic_send") -> None:
        """Schedule a periodic task"""
        try:
            # Remove existing job if it exists
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
            
            self.scheduler.add_job(
                func,
                IntervalTrigger(seconds=interval_seconds),
                id=job_id,
                name=f"Send messages every {interval_seconds} seconds"
            )
            logger.info(f"Scheduled periodic task: {job_id} every {interval_seconds} seconds")
        except Exception as e:
            logger.error(f"Error scheduling task: {e}")
    
    def schedule_once(self, func: Callable, delay_seconds: int) -> None:
        """Schedule a task to run once after delay"""
        try:
            run_time = datetime.now() + timedelta(seconds=delay_seconds)
            self.scheduler.add_job(func, 'date', run_date=run_time)
            logger.info(f"Scheduled one-time task in {delay_seconds} seconds")
        except Exception as e:
            logger.error(f"Error scheduling one-time task: {e}")
    
    def schedule_at_time(self, func: Callable, hour: int, minute: int) -> None:
        """Schedule a task at specific time daily"""
        try:
            self.scheduler.add_job(func, 'cron', hour=hour, minute=minute)
            logger.info(f"Scheduled daily task at {hour:02d}:{minute:02d}")
        except Exception as e:
            logger.error(f"Error scheduling daily task: {e}")
    
    def get_jobs(self) -> list:
        """Get all scheduled jobs"""
        return self.scheduler.get_jobs()
    
    def remove_job(self, job_id: str) -> bool:
        """Remove a scheduled job"""
        try:
            job = self.scheduler.get_job(job_id)
            if job:
                self.scheduler.remove_job(job_id)
                logger.info(f"Removed job: {job_id}")
                return True
        except Exception as e:
            logger.error(f"Error removing job: {e}")
        return False


class MessageQueue:
    """Queue for managing messages to be sent"""
    
    def __init__(self):
        self.queue = []
    
    def add_message(self, message_data: dict) -> None:
        """Add message to queue"""
        self.queue.append({
            "data": message_data,
            "added_at": datetime.now(),
            "sent": False
        })
        logger.info(f"Added message to queue. Queue size: {len(self.queue)}")
    
    def get_next_message(self) -> Optional[dict]:
        """Get next unsent message"""
        for msg in self.queue:
            if not msg["sent"]:
                return msg
        return None
    
    def mark_sent(self, message_data: dict) -> None:
        """Mark message as sent"""
        for msg in self.queue:
            if msg["data"] == message_data:
                msg["sent"] = True
                break
    
    def clear_sent_messages(self) -> None:
        """Remove sent messages from queue"""
        self.queue = [msg for msg in self.queue if not msg["sent"]]
    
    def get_queue_size(self) -> int:
        """Get current queue size"""
        return len([msg for msg in self.queue if not msg["sent"]])


# Global scheduler and queue
scheduler = MessageScheduler()
message_queue = MessageQueue()
