from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import yaml
from schedule import ScheduleConfig
from webhook import Webhook
import asyncio


async def weekly_job(config: ScheduleConfig, webhook: Webhook):
    if config.should_send():
        await webhook.send_message(config.message)


async def main():
    with open("config.yaml") as f:
        string_config = yaml.safe_load(f)

    scheduler_config = ScheduleConfig(**string_config["scheduler"])
    webhook = Webhook(**string_config["webhook"])
    tz = ZoneInfo(scheduler_config.timezone)
    scheduler = AsyncIOScheduler(timezone=tz)

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

    print("running...")
    scheduler.start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
