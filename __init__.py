import shutil
import sys
import logging

from pathlib import Path

from .manage import main


logger = logging.getLogger(__name__)

path = Path(__file__)
sys.path.append(str(path.parent))
sys.path.append(str(path.parent / "octopoes"))
sys.path.append(str(path.parent / "mula"))
sys.path.append(str(path.parent / "boefjes"))


def start(
    plugin_dir: str = "plugins",
):
    from boefjes.models import BOEFJES_DIR

    plugin_dir = Path() / plugin_dir

    if plugin_dir.exists():
        logger.info(f"Binding boefjes from directory {plugin_dir}")

        for plugin in plugin_dir.iterdir():
            if not plugin.is_dir:
                continue

            target = BOEFJES_DIR / ("_local_" + plugin.name)

            if target.exists():
                shutil.rmtree(target)

            shutil.copytree(plugin, target)

    try:
        sys.argv = ["manage.py", "runserver"]
        main()
    except KeyboardInterrupt:
        for plugin in BOEFJES_DIR.iterdir():
            if plugin.is_symlink():
                plugin.unlink()


