from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import yaml
from schedule import ScheduleConfig
from webhook import Webhook
import asyncio
from rich import traceback
from logger import setup_logging, logger


async def weekly_job(config: ScheduleConfig, webhook: Webhook):
    if config.should_send():
        logger.debug("Sending message")
        await webhook.send_message(config.message)
        logger.info("Message sent")


async def main():
    logger.debug("Reading config.yaml")
    with open("config.yaml") as f:
        string_config = yaml.safe_load(f)

    logger.debug("Setting up scheduler_config")
    scheduler_config = ScheduleConfig(**string_config["scheduler"])
    logger.debug("Setting up webhook")
    webhook = Webhook(**string_config["webhook"])
    tz = ZoneInfo(scheduler_config.timezone)
    scheduler = AsyncIOScheduler(timezone=tz)

    logger.info("Starting scheduler")
    scheduler.add_job(
        weekly_job,
        "cron",
        day_of_week=scheduler_config.send_day,
        hour=scheduler_config.send_time.hour,
        minute=scheduler_config.send_time.minute,
        args=[
            scheduler_config,
            webhook,
        ],
    )

    logger.info("Scheduler is running")
    scheduler.start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    traceback.install(show_locals=True, extra_lines=3)
    setup_logging()
    asyncio.run(main())
