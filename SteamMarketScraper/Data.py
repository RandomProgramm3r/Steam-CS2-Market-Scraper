from enum import Enum
from functools import lru_cache


class CS2Weapon(Enum):
    """
    This class represents the available weapons in CS2.
    """

    # Pistols
    GLOCK_18 = "Glock-18"
    USP_S = "USP-S"
    DESERT_EAGLE = "Desert Eagle"
    FIVE_SEVEN = "Five-SeveN"
    TEC9 = "Tec-9"
    P2000 = "P2000"
    DUAL_BERETTAS = "Dual Berettas"
    P250 = "P250"
    CZ75_AUTO = "CZ75-Auto"
    R8_REVOLVER = "R8 Revolver"

    # Rifle
    AK_47 = "AK-47"
    AUG = "AUG"
    M4A1S = "M4A1-S"
    M4A4 = "M4A4"
    FAMAS = "FAMAS"
    GALIL_AR = "Galil AR"
    SG_553 = "SG 553"

    # Sniper Rifle
    AWP = "AWP"
    SSG_08 = "SSG 08"
    G3SG1 = "G3SG1"
    SCAR_20 = "SCAR-20"

    # SMG
    MAC_10 = "MAC-10"
    MP5_SD = "MP5-SD"
    MP7 = "MP7"
    MP9 = "MP9"
    P90 = "P90"
    PP_BIZON = "PP-Bizon"
    UMP_45 = "UMP-45"

    # Shotgun
    NOVA = "Nova"
    SAWED_OFF = "Sawed-Off"
    MAG_7 = "MAG-7"
    XM1014 = "XM1014"

    # Machinegun
    M249 = "M249"
    NEGEV = "Negev"

    # Equipment
    ZEUS_x27 = "Zeus x27"

    # Knife
    BAYONET = "Bayonet"
    GUT_KNIFE = "Gut Knife"
    FLIP_KNIFE = "Flip Knife"
    KARAMBIT = "Karambit"
    M9_BAYONET = "M9 Bayonet"
    HUNTSMAN_KNIFE = "Huntsman Knife"
    BUTTERFLY_KNIFE = "Butterfly Knife"
    FALCHION_KNIFE = "Falchion Knife"
    BOWIE_KNIFE = "Bowie Knife"
    STILETTO_KNIFE = "Stiletto Knife"
    URSUS_KNIFE = "Ursus Knife"
    NAVAJA_KNIFE = "Navaja Knife"
    TALON_KNIFE = "Talon Knife"
    NOMAD_KNIFE = "Nomad Knife"
    KUKRI_KNIFE = "Kukri Knife"
    CLASSIC_KNIFE = "Classic Knife"
    PARACORD_KNIFE = "Paracord Knife"
    SHADOW_DAGGERS = "Shadow Daggers"
    SKELETON_KNIFE = "Skeleton Knife"
    SURVIVAL_KNIFE = "Survival Knife"

    @classmethod
    @lru_cache(maxsize=None)
    def get_all_weapon_names(cls) -> tuple[str, ...]:
        """
        Get a list of all weapon names available in CS2Weapon. (CS2)
        """
        return tuple(weapon.value for weapon in cls)

    # used so that when calling a class attribute without .value, an error does not occur in the function.
    def __str__(self) -> str:
        """
        Return the string representation of the CS2Weapon enum member.
        """
        return self.value


class CS2Agent(Enum):  # completed
    """
    A class representing the different types of CS2 agents.
    """

    THE_PROFESSIONALS = "The Professionals"
    GENDARMERIE_NATIONALE = "Gendarmerie Nationale"
    SABRE = "Sabre"
    FBI = "FBI"
    GUERRILLA_WARFARE = "Guerrilla Warfare"
    ELITE_CREW = "Elite Crew"
    SWAT = "SWAT"
    SEAL_FROGMAN = "SEAL Frogman"
    NSWC_SEAL = "NSWC SEAL"
    TACP_CAVALRY = "TACP Cavalry"
    USAF_TACP = "USAF TACP"
    FBI_SNIPER = "  FBI Sniper"
    PHOENIX = "Phoenix"
    FBI_HRT = "FBI HRT"

    # used so that when calling a class attribute without .value, an error does not occur in the function.
    def __str__(self) -> str:
        """
        Returns the string representation of the CS2AgentTypes enum value.
        """
        return self.value

    @classmethod
    @lru_cache(maxsize=None)
    def get_all_agent_types(cls) -> tuple[str, ...]:
        """
        Get a list of all agents available in CS2Weapon. (CS2)
        """
        return tuple(agents.value for agents in cls)


class Category(Enum):
    """
    They can be divided into the following categories:
     1) category | ...
     2) ... | category
     3) other
    """

    SOUVENIR = "Souvenir "
    STATTRAK = "StatTrak™ "
    PATCH = "Patch"
    MUSIC_KIT = "Music Kit"
    STATTRAK_MUSIC_KIT = "StatTrak™ Music Kit"
    STATTRAK_KNIFE = "stattrak knife"
    KNIFE = "knife"
    STICKER = "Sticker"
    SEALED_GRAFFITI = "Sealed Graffiti"

    HYDRA_GLOVES = "★ Hydra Gloves"
    BLOODHOUND_GLOVES = "★ Bloodhound Gloves"
    BROKEN_FANG_GLOVES = "★ Broken Fang Gloves"
    DRIVER_GLOVES = "★ Driver Gloves"
    HAND_WRAPS = "★ Hand Wraps"
    MOTO_GLOVES = "★ Moto Gloves"
    SPORT_GLOVES = "★ Sport Gloves"
    SPECIALIST_GLOVES = "★ Specialist Gloves"
    # 2)
    CASE = "Case"
    SOUVENIR_PACKAGE = "Souvenir Package"
    PIN = "Pin"

    CAPSULE_KEY = "Key"
    CASE_KEY = "Case Key"

    PASS = "Pass"
    VIEWER_PASS = "Viewer Pass"
    VIEWER_PASS_PLUS_3_TOKENS = "Viewer Pass + 3 Souvenir Tokens"

    AGENT = "Agent"
    MUSIC_KIT_BOX = "Music Kit Box"
    STATTRAK_MUSIC_KIT_BOX = "StatTrak Music Kit Box"

    STICKER_CAPSULE = "Sticker Capsule"
    AUTOGRAPH_CAPSULE = "Autograph Capsule"
    # 3)
    ANY = "Any"

    # used so that when calling a class attribute without .value, an error does not occur in the function.
    def __str__(self) -> str:
        """
        Returns the string representation of the CS2AgentTypes enum value.
        """
        return self.value

    @classmethod
    @lru_cache(maxsize=None)
    def get_all_categories(cls) -> tuple[str, ...]:
        """
        Get a list of all agents available in CS2Weapon. (CS2)
        """
        return tuple(categories.value for categories in cls)


class Major(Enum):
    """
    An enumeration representing various CS:GO and CS2 Major tournaments.

    The `Major` class is an `Enum` that encapsulates the CS:GO Major tournaments and their corresponding names.
    """
    PGL_COPENHAGEN_2024 = "Copenhagen 2024"
    BLAST_TV_PARIS_2023 = 'Paris 2023'
    PGL_ANTWERP_2022 = "Antwerp 2022"
    IEM_RIO_2022 = "Rio 2022"
    PGL_STOCKHOLM_2021 = "Stockholm 2021"
    RMR_2020 = "RMR 2020"
    STAR_LADDER_BERLIN = "Berlin 2019"
    IEM_KATOWICE_2019 = "Katowice 2019"
    ELEAGUE_BOSTON_2018 = "Boston 2018"
    FACEIT_LONDON_2018 = "London 2018"
    PGL_KRAKOW_2017 = "Krakow 2017"
    ELEAGUE_ATLANTA_2017 = "Atlanta 2017"
    ESL_ONE_COLOGNE_2016 = "Cologne 2016"
    MLG_COLUMBUS_2016 = "MLG Columbus 2016"
    DREAMHACK_CLUJ_NAPOCA_2015 = "Cluj-Napoca 2015"
    ESL_ONE_COLOGNE_2015 = "Cologne 2015"
    ESL_ONE_KATOWICE_2015 = "Katowice 2015"
    ESL_ONE_COLOGNE_2014 = "Cologne 2014"
    EMS_ONE_KATOWICE_2014 = "Katowice 2014"
    DREAMHACK_WINTER_2014 = "DreamHack 2014"
    DREAMHACK_WINTER_2013 = "DreamHack 2013"

    @classmethod
    @lru_cache(maxsize=None)
    def get_all_majors(cls) -> tuple[str, ...]:
        """
        Get a list of all CS:GO and CS2 Major tournaments.
        """
        return tuple(agents.value for agents in cls)

    # used so that when calling a class attribute without .value, an error does not occur in the function.
    def __str__(self) -> str:
        """
        Return the string representation of the quality.
        """
        return self.value


class CS2Qualities(Enum):
    """
    An enumeration representing various qualities for CS2 items.

    The `CS2Qualities` class is an `Enum` that encapsulates the possible qualities for CS2 items.

    Methods:
    __str__(): Returns the string representation of the quality.
    get_qualities(): Returns a tuple of all available qualities.
    validate_quality(quality: str): Checks if a given quality string is valid.
    """

    # CS2 item qualities
    FACTORY_NEW = "(Factory New)"
    MINIMAL_WEAR = "(Minimal Wear)"
    FIELD_TESTED = "(Field-Tested)"
    WELL_WORN = "(Well-Worn)"
    BATTLE_SCARED = "(Battle-Scarred)"
    NOT_PAINTED = "(Not Painted)"

    # patch & sticker
    GOLD = "(Gold)"

    # sticker
    GLITTER = "(Glitter)"
    HOLO = "(Holo)"
    FOIL = "(Foil)"
    LENTICULAR = "(Lenticular)"
    CHAMPION = "(Champion)"
    CHAMPION_GOLD = "(Gold, Champion)"
    CHAMPION_HOLO = "(Holo, Champion)"
    CHAMPION_GLITTER = "(Glitter, Champion)"

    # Sealed Graffiti
    TRACER_YELLOW = "(Tracer Yellow)"
    BLOOD_RED = "(Blood Red)"
    TIGER_ORANGE = "(Tiger Orange)"
    DUST_BROWN = "(Dust Brown)"
    DESERT_AMBER = "(Desert Amber)"
    BRICK_RED = "(Brick Red)"
    WAR_PIG_PINK = "(War Pig Pink)"
    BAZOOKA_PINK = "(Bazooka Pink)"
    PRINCESS_PINK = "(Princess Pink)"
    MONSTER_PURPLE = "(Monster Purple)"
    CASH_GREEN = "(Cash Green)"
    BATTLE_GREEN = "(Battle Green)"
    JUNGLE_GREEN = "(Jungle Green)"
    FROG_GREEN = "(Frog Green)"
    SHARK_WHITE = "(Shark White)"
    WIRE_BLUE = "(Wire Blue)"
    MONARCH_BLUE = "(Monarch Blue)"
    SWAT_BLUE = "(SWAT Blue)"
    VIOLENT_VIOLET = "(Violent Violet)"

    # used so that when calling a class attribute without .value, an error does not occur in the function.
    def __str__(self) -> str:
        """
        Return the string representation of the quality.
        """
        return self.value

    @classmethod
    @lru_cache(maxsize=None)
    def get_qualities(cls) -> tuple:
        """
        Get the list of available qualities.
        """
        return tuple(member.value for member in cls)


class Currency(Enum):
    """
    An enumeration representing various currencies.

    The `Currency` class is an `Enum` that encapsulates the ISO 4217a currency codes and their corresponding names.

    """
    # ISO 4217a
    USD = 1  # United States dollar
    GBP = 2  # Pound sterling
    EUR = 3  # Euro
    CHF = 4  # Swiss franc
    RUB = 5  # Russian ruble
    PLN = 6  # Polish złoty
    BRL = 7  # Brazilian real
    JPY = 8  # Japanese yen
    SEK = 9  # Swedish króna
    IDR = 10  # Indonesian rupiah
    MYR = 11  # Malaysian ringgit
    PHP = 12  # Philippine peso
    SGD = 13  # Singapore dollar
    THB = 14  # Thai baht
    VND = 15  # Vietnamese đồng
    KRW = 16  # South Korean won
    TRY = 17  # Turkish lira
    UAH = 18  # Ukrainian hryvnia
    MXN = 19  # Mexican peso
    CAD = 20  # Canadian dollar
    AUD = 21  # Australian dollar
    NZD = 22  # New Zealand dollar
    CNY = 23  # Renminbi
    INR = 24  # Indian rupee
    CLP = 25  # Chilean peso
    CUP = 26  # Cuban peso
    COP = 27  # Colombian peso
    ZAR = 28  # South African rand
    HKD = 29  # Hong Kong dollar
    TWD = 30  # New Taiwan dollar
    SAR = 31  # Saudi riyal
    AED = 32  # United Arab Emirates dirham
    # -
    ARS = 34  # Argentine peso
    ILS = 35  # Israeli new shekel
    # -
    KZT = 37  # Kazakhstani tenge
    KWD = 38  # Kuwaiti dinar
    QAR = 39  # Qatari riyal
    CRC = 40  # Costa Rican colon

    @classmethod
    @lru_cache(maxsize=None)
    def get_all_currencies(cls) -> tuple:
        """
        Get the list of available currencies.
        """
        return tuple(member for member in vars(cls) if not member.startswith("_") and not member.startswith("g"))
