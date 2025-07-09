from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot import messageFlow

scheduler = AsyncIOScheduler()

def startScheduler():
    trigger = CronTrigger(day_of_week='mon-thu', hour=22, minute=0)
    scheduler.add_job(messageFlow, trigger)
    scheduler.start()
