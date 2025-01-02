import asyncio
import argparse
import logging
from pathlib import Path
import shutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("main.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


async def copy_file(source_path: Path, dest_path: Path):
    try:
        extension = (
            source_path.suffix[1:].lower() if source_path.suffix else "no_extension"
        )

        extension_folder = dest_path / extension
        extension_folder.mkdir(exist_ok=True)

        destination = extension_folder / source_path.name

        await asyncio.to_thread(shutil.copy2, source_path, destination)
        logger.info(f"Скопійовано файл: {source_path} -> {destination}")

    except Exception as e:
        logger.error(f"Помилка при копіюванні файлу {source_path}: {str(e)}")


async def read_folder(source_path: Path, dest_path: Path):
    try:
        tasks = []

        for item in source_path.rglob("*"):
            if item.is_file():
                task = asyncio.create_task(copy_file(item, dest_path))
                tasks.append(task)

        if tasks:
            await asyncio.gather(*tasks)

    except Exception as e:
        logger.error(f"Помилка при читанні папки {source_path}: {str(e)}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Шляхи до вихідної та цільової папок для сортування файлів"
    )
    parser.add_argument("source", type=str, help="Шлях до вихідної папки")
    parser.add_argument("destination", type=str, help="Шлях до цільової папки")
    return parser.parse_args()


async def main():

    args = parse_arguments()

    source_path = Path(args.source)
    dest_path = Path(args.destination)

    if not source_path.exists():
        logger.error(f"Вихідна папка не існує: {source_path}")
        return

    dest_path.mkdir(exist_ok=True)

    logger.info(
        f"Початок сортування та копіювання файлів з {source_path} в {dest_path}"
    )

    await read_folder(source_path, dest_path)

    logger.info("Сортування та копіювання файлів завершено")


if __name__ == "__main__":
    asyncio.run(main())
