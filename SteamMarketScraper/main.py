from MarketScraper import (Category,
                           Currency,
                           CS2Agent,
                           CS2Weapon,
                           CS2Qualities,
                           Major)
from MarketScraper import Market_Scraper


"""
Scraper version 1.0

Some examples of using the scraper
"""

if __name__ == '__main__':
    print(Market_Scraper(
        "paw",
        quality=CS2Qualities.FACTORY_NEW.value,
        category=Category.STATTRAK.value,
        weapon=CS2Weapon.AWP.value))

    print(Market_Scraper(
        "Dreams & Nightmares Case",
        category=Category.ANY.value,
        currency=Currency.EUR.value))

    print(Market_Scraper(
        "furia",
        category=Category.STICKER.value,
        quality=CS2Qualities.HOLO.value,
        major=Major.PGL_ANTWERP_2022.value))

    print(Market_Scraper(
        "Sir Bloody Miami Darryl",
        category=Category.AGENT.value,
        agent_type=CS2Agent.THE_PROFESSIONALS.value))

    print(Market_Scraper(
        "Paris 2023 Anubis",
        category=Category.SOUVENIR_PACKAGE.value,
        currency=Currency.GBP.value))
