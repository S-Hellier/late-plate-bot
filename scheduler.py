# scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot import sendGroupMeMessage

scheduler = AsyncIOScheduler()

def startScheduler():
    # Schedules a job for every weekday at 9:00 AM (adjust to your timezone)
    trigger = CronTrigger(day_of_week='mon-fri', hour=9, minute=0)
    
    scheduler.add_job(sendGroupMeMessage, trigger, args=["Good morning from your FastAPI bot!"])
    scheduler.start()
