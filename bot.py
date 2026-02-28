#!/usr/bin/env python3
"""Web3 Automation Bot — Main Entry Point"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PLATFORM = os.getenv("PLATFORM", "telegram")

if __name__ == "__main__":
    if PLATFORM == "telegram":
        from platforms.telegram_bot import run_telegram
        logger.info("Starting Telegram bot...")
        run_telegram()
    elif PLATFORM == "discord":
        from platforms.discord_bot import run_discord
        logger.info("Starting Discord bot...")
        run_discord()
    else:
        logger.error(f"Unknown platform: {PLATFORM}")
