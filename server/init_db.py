"""Utility script to drop and recreate all tables."""
import asyncio

from src.core.database import init


def main() -> None:
    asyncio.run(init())


if __name__ == "__main__":
    main()
