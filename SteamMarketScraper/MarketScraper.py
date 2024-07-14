from Data import (CS2Weapon,
                  CS2Agent,
                  Category,
                  Major,
                  CS2Qualities,
                  Currency)
import urllib.request
import urllib.error
import json
import time
import logging
import threading
from urllib.parse import quote_plus
from collections import OrderedDict
from typing import Callable, Union


class Cache:
    def __init__(self, max_size=100, ttl=60):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl
        self.lock = threading.Lock()

    def get(self, name, currency):
        with self.lock:
            cache_key = (name, currency)
            if cache_key in self.cache:
                if time.monotonic() - self.cache[cache_key]['time'] < self.ttl:
                    self.cache.move_to_end(cache_key)
                    return self.cache[cache_key]["cached_name"]
                else:
                    del self.cache[cache_key]
            return None

    def set(self, name, currency, cached_name):
        with self.lock:
            cache_key = (name, currency)
            self.cache[cache_key] = {
                "cached_name": cached_name,
                "time": time.monotonic()
            }
            self.cache.move_to_end(cache_key)


class Replacements:
    def __init__(self):
        self.replacements = {}
        self.load_replacements()

    def load_replacements(self):
        try:
            with open('replacements/all_replacements.json', 'r', encoding="utf-8") as f:
                self.replacements = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading replacements: {e}")

    def replace_values(self, value: str) -> str:
        """
        This function replaces substrings in a given input value based on the loaded replacements.
        It is designed to make the process case-insensitive.

        :parameter value: The string to be processed

        :returns: The processed string with all replacements made, or the original value if no replacements are found
        """
        if not self.replacements:
            return value

        for old_str, new_str in self.replacements.items():
            value = value.replace(old_str, new_str)
        return value


def validate_name_input(input_string: str, min_length=1, max_length=50) -> str:
    """
    Function to validate an input string representing a name.

    Arguments:
    :param input_string: The input string to be validated.
    :param min_length: The minimum allowed length for the input string. Defaults to 1.
    :param max_length: The maximum allowed length for the input string. Defaults to 50.

    Description:
    Validates input string:
    Ensures non-empty, non-space only.
    Checks length within [min_length, max_length].
    Verifies characters as English letters, numbers, or special characters

    :returns: The input string if it passes validation, otherwise an error message.
    """
    import string

    some_allowed_characters = " 弐壱™花脸龍王|★"

    if not input_string.strip():
        return "The name cannot be empty or contain only spaces."

    if not min_length <= len(input_string) <= max_length:
        return f"Enter a name between {min_length} and {max_length} characters."

    allowed_chars = string.ascii_letters + string.digits + string.punctuation + some_allowed_characters

    for char in input_string:
        if char not in allowed_chars:
            return "The string contains invalid characters."

    return input_string


def validate_input_types(currency, quality, category, agent_type, weapon, major) -> None:
    """
    Validates the types of the input parameters.

    :param currency: The currency type, which can be an instance of Currency, an integer, or a string.
    :param quality: The quality type, which can be an instance of CS2Qualities or a string.
    :param category: The category type, which can be an instance of Category or a string.
    :param agent_type: The agent type, which can be an instance of CS2Agent or a string.
    :param weapon: The weapon type, which can be an instance of CS2Weapon or a string.
    :param major: The major type, which can be an instance of Major or a string.

    :raise TypeError: If any of the input parameters do not match the expected types.

    :returns: None
    """
    if (not isinstance(currency, (Currency, int, str))
            or not isinstance(quality, (CS2Qualities, str))
            or not isinstance(category, (Category, str))
            or not isinstance(agent_type, (CS2Agent, str))
            or not isinstance(weapon, (CS2Weapon, str))
            or not isinstance(major, (Major, str))):
        raise TypeError("Invalid input type detected.")
    return None


def process_input(name, currency, quality, category, agent_type, weapon, major):
    validation_result = validate_name_input(name)
    if validation_result != name:
        return validation_result

    validate_input_types(currency, quality, category, agent_type, weapon, major)

    return True


def load_name_creation_logic(
        name: str,
        quality: Union[CS2Qualities, str] = "",
        category: Union[Category, str] = "",
        agent_type: Union[CS2Agent, str] = "",
        weapon: Union[CS2Weapon, str] = "",
        major: Union[Major, str] = "") -> dict[str, Callable[[], str]]:

    """
    Loads the logic for creating names based on the provided parameters.
    :returns: A dictionary mapping keys to lambda functions that generate names based on the provided parameters.
    """

    name_creation_logic: dict[str, Callable[[], str]] = {
                "any":
                lambda: f"{name}",

                "default name":
                lambda:
                f"{category}{weapon} | {name}{' ' + quality if quality else ''}{' | ' + major if major else major}",

                "knife":
                lambda: f"★ {weapon}{' | ' + name if quality != '' else ' ' + name} {quality}",

                "stattrak knife":
                lambda: f"★ StatTrak™ {weapon}{' | ' + name if quality != '' else ' ' + name} {quality}",

                "case":
                lambda: f"{name} {category}",

                "pin":
                lambda: f"{name} {category}",

                "souvenir package":
                lambda: f"{major + ' ' if major else ''}{name} {category}",

                "pass":
                lambda: f"{name} {category}",

                "viewer pass":
                lambda: f"{name} {category}",

                "viewer pass + 3 souvenir tokens":
                lambda: f"{name} {category}",

                "agent":
                lambda: f"{name}{' | ' + agent_type}" if agent_type else name,

                "case key":
                lambda: f"{name} {category}",

                "key":
                lambda: f"{name} {category}",

                "sticker":
                lambda: f"{category} | {name}{' ' + quality if quality else ''}{' | ' + major if major else ''}",

                "patch":
                lambda: f"{category} | {name}{' ' + quality if quality else ''}{' | ' + major if major else ''}",

                "stattrak music kit box":
                lambda: f"StatTrak™ {name} Music Kit Box",

                "music kit box":
                lambda: f"{name} {category}",

                "sticker capsule":
                lambda: f"{major} {name} {category}",

                "autograph capsule":
                lambda: f"{category} | {name} {quality} | {major}"
                        if major in [
                                Major.DREAMHACK_CLUJ_NAPOCA_2015.value,
                                Major.ESL_ONE_COLOGNE_2015.value,
                                Major.ESL_ONE_COLOGNE_2016.value,
                                Major.MLG_COLUMBUS_2016.value,
                                Major.ELEAGUE_ATLANTA_2017.value,
                                Major.PGL_KRAKOW_2017.value
                            ] else f"{major} {name} {category}"
            }

    return name_creation_logic


def create_name(name_creation_logic: dict[str, Callable[[], str]], category: Union[Category, str] = "") -> str:
    item_type_information = category.strip().lower()
    return name_creation_logic.get(item_type_information, name_creation_logic["default name"])()


def process_name(name: str) -> str:
    """
    Normalize  the given name.

    :param name: The name to be processed.

    :return: The processed  name.
    """

    # converting to title case, and joining words with a single space.
    normalized_name = " ".join(name.strip().title().split())

    return normalized_name


def encode_name(normalized_name: str) -> str:
    """
    Encode the given name.

    :param normalized_name: The name to be encoded.

    :returns:  The encoded name.
    """

    # URL-encode the normalized name, replacing spaces with '+'
    encoded_name = quote_plus(normalized_name).replace("~", "%7E")

    return encoded_name


def fetch_data(encoded_name: str, currency: int = Currency.USD) -> dict[str]:
    """
    Fetches market price data from the Steam Community Market for a specified item.

    This function constructs a URL based on the provided item name (encoded) and currency,
    then sends a request to the Steam Community Market API to retrieve price overview data.

    :param encoded_name: The URL-encoded name of the item to fetch price data for.
    :param currency: The currency code (default is USED) in which the price data should be returned.

    :returns: A dictionary containing the price overview data for the specified item.
    """
    base_url = "https://steamcommunity.com/market/priceoverview/?appid=730"
    with urllib.request.urlopen(
            f"{base_url}&currency={currency}&market_hash_name={encoded_name}"
    ) as url:
        # Read the response and decode it
        response = url.read().decode()
        # Parse the JSON data
        data = json.loads(response)
        return data


def generate_processed_name(
        name: str,
        quality: Union[CS2Qualities, str] = "",
        category: Union[Category, str] = "",
        agent_type: Union[CS2Agent, str] = "",
        weapon: Union[CS2Weapon, str] = "",
        major: Union[Major, str] = "") -> str:
    # Loads the name creation logic based on the provided parameters
    name_creation_logic = load_name_creation_logic(name, quality, category, agent_type, weapon, major)
    if not name_creation_logic:
        raise ValueError("Error loading name creation logic")
    # Creates the name based on the loaded logic and category
    name = create_name(name_creation_logic, category)
    # Processes the name
    name = process_name(name)
    # Encodes the name for the request to the server
    name = encode_name(name)
    # Replaces values in the name using the replacer object
    name = replacer.replace_values(name)
    return name


def get_cached_value(_cache: Cache, name: str, currency: Union[CS2Agent, str, int]):
    """
    Retrieves the cached value for a given item name and currency.

    :param _cache: The cache object used to store and retrieve cached values.
    :param name: The name of the item.
    :param currency: The currency in which the item's price is specified.

    :returns: The cached value if it exists, otherwise None.
    """
    return _cache.get(name, currency)


def fetch_lowest_price(name: str, currency: Union[CS2Agent, str, int]) -> str:
    """
    Fetches the lowest price for a given item name and currency from an external data source.

    :param name: The name of the item.
    :param currency: The currency in which the item's price is specified.

    :returns: The lowest price of the item, or a message indicating that the item is not currently being sold.
    """
    data = fetch_data(name, currency)
    return data.get("lowest_price", "No one is selling this item right now")


def format_result(category, original_name, quality, lowest_price) -> str:
    """
    Formats the result string with the given category, original name, quality, and lowest price.

    :param category: The category of the item.
    :param original_name: The original name of the item.
    :param quality: The quality of the item.
    :param lowest_price: The lowest price of the item.

    :returns: A formatted string containing the item's details and lowest price.
    """
    return " ".join(
        f"{category if category else ''} {original_name + ',' if not quality else original_name} "
        f"{quality + ',' if quality else ''} correct price: {lowest_price}.".strip().title().split())


def set_cache(_cache, name, currency, result) -> None:
    """
    Sets the cache with the given item name, currency, and result.

    :param _cache: The cache object used to store and retrieve cached values.
    :param name: The name of the item.
    :param currency: The currency in which the item's price is specified.
    :param result: The result string to be cached.

    :returns: None
    """
    _cache.set(name, currency, result)


def get_item_info(
        _cache: Cache,
        name: str,
        original_name: str,
        currency: Union[Currency, int, str],
        category: Union[Category, str],
        quality: Union[CS2Qualities, str]) -> str:
    """
    Retrieves the item information, either from the cache or by fetching the lowest price and formatting the result.

    :param _cache: The cache object used to store and retrieve cached values.
    :param name: The name of the item.
    :param original_name: The original name of the item.
    :param currency: The currency in which the item's price is specified.
    :param category: The category of the item.
    :param quality: The quality of the item.

    :returns: The item information, either from the cache or freshly fetched and formatted.
    """
    cached_value = get_cached_value(cache, name, currency)
    if cached_value:
        return cached_value

    lowest_price = fetch_lowest_price(name, currency)
    result = format_result(category, original_name, quality, lowest_price)
    set_cache(cache, name, currency, result)
    return result


replacer = Replacements()
cache = Cache(max_size=100, ttl=60)


def Market_Scraper(
        name: str,
        currency: Union[Currency, int, str] = Currency.USD.value,
        quality: Union[CS2Qualities, str] = "",
        category: Union[Category, str] = "",
        agent_type: Union[CS2Agent, str] = "",
        weapon: Union[CS2Weapon, str] = "",
        major: Union[Major, str] = "") -> str:
    """version 1.0"""

    result = process_input(name, currency, quality, category, agent_type, weapon, major)
    if result is not True:
        return result

    original_name: str = process_name(name)

    try:
        name: str = generate_processed_name(name, quality, category, agent_type, weapon, major)

        result: str = get_item_info(cache, name, original_name, currency, category, quality)

    except KeyError as e:
        logging.error(f"KeyError occurred: {e}")
        return "There were no items matching your search. Try again with different keywords."
    except ValueError as e:
        logging.error(f"KeyError occurred: {e}")
        return "Error loading name creation logic"
    except urllib.error.HTTPError as e:
        logging.error(f"HTTPError occurred: {e}")
        return "There was an issue with the server. Please try again later."

    return result
