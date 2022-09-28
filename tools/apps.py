import sys
import time
import logging
from threading import Thread

from django.apps import AppConfig

from boefjes.tasks import handle_boefje, handle_normalizer
from scheduler import App, context
from scheduler.models import BoefjeTask, NormalizerTask

logger = logging.getLogger(__name__)
scheduler_app = App(context.AppContext())


def boefjes_task_listener():
    while True:
        for scheduler in scheduler_app.schedulers.values():
            if scheduler.queue.empty():
                continue

            p_item = scheduler.queue.pop()
            logger.info(f"Handling task: {p_item}")

            if isinstance(p_item.item, BoefjeTask):
                Thread(target=handle_boefje, args=(p_item.item.dict(),)).start()

            if isinstance(p_item.item, NormalizerTask):
                Thread(target=handle_normalizer, args=(p_item.item.dict(),)).start()

        time.sleep(1)


class ToolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tools"

    def ready(self):
        if "runserver" in sys.argv:
            Thread(target=scheduler_app.run).start()
            Thread(target=boefjes_task_listener).start()
