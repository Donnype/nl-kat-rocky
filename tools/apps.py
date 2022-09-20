import sys
import time
import logging
from threading import Thread

from django.apps import AppConfig

from boefjes.tasks import handle_boefje, handle_normalizer
from scheduler import App, context
from scheduler.dispatchers.dispatcher import TASKS


logger = logging.getLogger(__name__)
scheduler_app = App(context.AppContext())


def boefjes_task_listener():
    while True:
        for queue_name, queue_tasks in TASKS.items():
            if not queue_tasks:
                continue

            for task_name, tasks in queue_tasks.items():
                if not tasks:
                    continue

                task = tasks.pop(0)
                logger.info(f"Handling task: {task}")

                if "boefje" in queue_name:
                    process = Thread(target=handle_boefje, args=(task,))
                    process.start()

                if "normalizer" in queue_name:
                    process = Thread(target=handle_normalizer, args=(task,))
                    process.start()

        time.sleep(1)


class ToolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tools"

    def ready(self):
        if "runserver" in sys.argv:
            Thread(target=scheduler_app.run).start()
            Thread(target=boefjes_task_listener).start()
