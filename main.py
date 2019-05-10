import asyncio
import logging
from submissions import get_new_submission
from cron_jobs.five_minutes import five_minutes_cron
from cron_jobs.one_hour import one_hour_cron
from cron_jobs.daily import daily_cron
from cron_jobs.weekly import weekly_cron
logging.basicConfig(level=logging.ERROR, filename='log.log')
logger = logging.getLogger(__name__)
logger.info("Start loop")
loop = asyncio.get_event_loop()
loop.run_forever()
loop.create_task(get_new_submission())
loop.create_task(five_minutes_cron())
loop.create_task(one_hour_cron())
loop.create_task(daily_cron())
loop.create_task(weekly_cron())
