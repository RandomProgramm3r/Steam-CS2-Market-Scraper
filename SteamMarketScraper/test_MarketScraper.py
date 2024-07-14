import unittest
import time
from MarketScraper import (Category,
                           Currency,
                           CS2Agent,
                           CS2Weapon,
                           CS2Qualities,
                           Major)
from MarketScraper import (Market_Scraper,
                           Cache,
                           Replacements,
                           validate_name_input,
                           validate_input_types,
                           process_input,
                           process_name,
                           encode_name,
                           fetch_data)


# overestimated parameters for the test
max_size = 150
ttl = 360

replacer = Replacements()
cache = Cache(max_size=max_size, ttl=ttl)


class TestCache(unittest.TestCase):
    print(f"max input size: {max_size} \ntime to life of cache: {ttl}")

    def test_market_scraper_performance(self):

        start = time.time()
        result = Market_Scraper(
            "Black Lotus",
            weapon=CS2Weapon.M4A1S.value,
            quality=CS2Qualities.FACTORY_NEW.value
        )
        end = time.time()
        print(f"First call result: {result}")
        print(f"First call time: {end - start}")

        start = time.time()
        result = Market_Scraper(
            "Black Lotus",
            weapon=CS2Weapon.M4A1S.value,
            quality=CS2Qualities.FACTORY_NEW.value
        )
        end = time.time()
        print(f"Second call result: {result}")
        print(f"Second call time: {end - start}")


class TestValidateNameInput(unittest.TestCase):

    def test_valid_name(self):
        self.assertEqual(validate_name_input("Cortex"), "Cortex")

    def test_empty_string(self):
        self.assertEqual(validate_name_input(""), "The name cannot be empty or contain only spaces.")

    def test_only_spaces(self):
        self.assertEqual(validate_name_input("     "), "The name cannot be empty or contain only spaces.")

    def test_too_long(self):
        long_name = "A" * 51
        self.assertEqual(validate_name_input(long_name, min_length=1, max_length=50),
                         "Enter a name between 1 and 50 characters.")

    def test_invalid_characters(self):
        self.assertEqual(validate_name_input("猫"), "The string contains invalid characters.")
        self.assertEqual(validate_name_input("Kočka"), "The string contains invalid characters.")

    def test_special_characters(self):
        self.assertEqual(validate_name_input("StatTrak™ AWP | Atheris"), "StatTrak™ AWP | Atheris")

    def test_numbers(self):
        self.assertEqual(validate_name_input("Gamma 2"), "Gamma 2")


class TestValidateNameInputType(unittest.TestCase):
    def test_valid_inputs(self):
        try:
            validate_input_types(
                currency=Currency.EUR,
                quality=CS2Qualities.FACTORY_NEW,
                category=Category.ANY,
                agent_type=CS2Agent.ELITE_CREW,
                weapon=CS2Weapon.AWP.value,
                major=Major.PGL_STOCKHOLM_2021)
        except TypeError:
            self.fail("validate_input_types() raised TypeError unexpectedly!")

    def test_invalid_currency_type(self):
        # Check that the function raises an exception with an invalid type for currency
        with self.assertRaises(TypeError):
            validate_input_types(
                currency=11.6000,
                quality=CS2Qualities.FACTORY_NEW,
                category=Category.ANY,
                agent_type=CS2Agent.ELITE_CREW,
                weapon=CS2Weapon.AWP.value,
                major=Major.PGL_STOCKHOLM_2021)

    def test_invalid_quality_type(self):
        # Check that the function raises an exception with an invalid type for quality
        with self.assertRaises(TypeError):
            validate_input_types(
                currency=Currency.EUR,
                quality=True,
                category=Category.ANY,
                agent_type=CS2Agent.ELITE_CREW,
                weapon=CS2Weapon.AWP.value,
                major=Major.PGL_STOCKHOLM_2021)

    def test_invalid_category_type(self):
        # Check that the function raises an exception with an invalid type for category
        with self.assertRaises(TypeError):
            validate_input_types(
                currency=Currency.EUR,
                quality=CS2Qualities.FACTORY_NEW,
                category=["cat"],
                agent_type=CS2Agent.ELITE_CREW,
                weapon=CS2Weapon.AWP.value,
                major=Major.PGL_STOCKHOLM_2021)

    def test_invalid_agent_type_type(self):
        # Check that the function raises an exception with an invalid type for agent_type
        with self.assertRaises(TypeError):
            validate_input_types(
                currency=Currency.EUR.value,
                quality=CS2Qualities.FACTORY_NEW,
                category=Category.ANY,
                agent_type=range(10),
                weapon=CS2Weapon.AWP.value,
                major=Major.PGL_STOCKHOLM_2021)

    def test_invalid_weapon_type(self):
        # Check that the function raises an exception with an invalid type for weapon
        with self.assertRaises(TypeError):
            validate_input_types(
                currency=Currency.EUR,
                quality=CS2Qualities.FACTORY_NEW,
                category=Category.ANY,
                agent_type=CS2Agent.ELITE_CREW,
                weapon={"banana"},
                major=Major.PGL_STOCKHOLM_2021)

    def test_invalid_major_type(self):
        # Check that the function raises an exception with an invalid type for major
        with self.assertRaises(TypeError):
            validate_input_types(
                currency=Currency.EUR,
                quality=CS2Qualities.FACTORY_NEW,
                category=Category.ANY,
                agent_type=CS2Agent.ELITE_CREW,
                weapon=CS2Weapon.AWP.value,
                major=None)


class TestProcessInput(unittest.TestCase):
    def test_successful_process_input(self):
        result = process_input(
                name="Black Lotus",
                currency=Currency.EUR.value,
                quality=CS2Qualities.FACTORY_NEW.value,
                category=Category.ANY.value,
                agent_type=CS2Agent.ELITE_CREW.value,
                weapon=CS2Weapon.AWP.value,
                major=Major.PGL_STOCKHOLM_2021.value)
        self.assertTrue(result)

    def test_invalid_name(self):
        result = process_input(
            "",
            weapon=CS2Weapon.M4A1S.value,
            quality=CS2Qualities.FACTORY_NEW.value,
            currency=Currency.EUR,
            category="",
            agent_type="",
            major=""
        )
        self.assertEqual(result, "The name cannot be empty or contain only spaces.")

    def test_invalid_types(self):
        with self.assertRaises(TypeError):
            validate_input_types(
                currency=Currency.EUR,
                quality=CS2Qualities.FACTORY_NEW,
                category=Category.ANY,
                agent_type=CS2Agent.ELITE_CREW,
                weapon=CS2Weapon.AWP.value,
                major=None)


class TestProcessName(unittest.TestCase):
    def test_letter_case(self):
        input_string = "bLAck lotUS"
        expected_output = "Black Lotus"
        self.assertEqual(process_name(input_string), expected_output)

    def test_extra_spaces(self):
        input_string = "   Temukau           "
        expected_output = "Temukau"
        self.assertEqual(process_name(input_string), expected_output)

    def test_spaces_between_words(self):
        input_string = "Bad     News     Eagles"
        expected_output = "Bad News Eagles"
        self.assertEqual(process_name(input_string), expected_output)

    def test_full_process(self):
        input_string = "   oPeratiOn    broKen   faNG   "
        expected_output = "Operation Broken Fang"
        self.assertEqual(process_name(input_string), expected_output)


class TestEncodeName(unittest.TestCase):
    def test_basic_weapon(self):
        self.assertEqual(encode_name("AK-47"), "AK-47")

    def test_name_with_spaces(self):
        self.assertEqual(encode_name("AWP | Dragon Lore"), "AWP+%7C+Dragon+Lore")

    def test_name_with_special_characters(self):
        self.assertEqual(encode_name("★ Karambit | Doppler"), "%E2%98%85+Karambit+%7C+Doppler")

    def test_name_with_stattrak(self):
        self.assertEqual(encode_name("StatTrak™ AK-47 | Redline"), "StatTrak%E2%84%A2+AK-47+%7C+Redline")

    def test_name_with_tilde(self):
        self.assertEqual(encode_name("Music Kit | Chipzel, ~Yellow Magic~"),
                         "Music+Kit+%7C+Chipzel%2C+%7EYellow+Magic%7E")

    def test_name_with_mixed_characters(self):
        self.assertEqual(encode_name("★ StatTrak™ M9 Bayonet | Crimson Web"),
                         "%E2%98%85+StatTrak%E2%84%A2+M9+Bayonet+%7C+Crimson+Web")


class TestReplaceValues(unittest.TestCase):
    replacer = Replacements()

    def test_basic_replacement(self):
        self.assertEqual(TestReplaceValues.replacer.replace_values("Awp+Paw"), "AWP+PAW")

    def test_no_replacements(self):
        self.assertEqual(TestReplaceValues.replacer.replace_values("CS20+Case"), "CS20+Case")

    def test_replace_values_partial_replacements(self,):
        self.assertEqual(TestReplaceValues.replacer.replace_values("Jungle+Ddpat+Pandora%27S+Box"),
                         "Jungle+DDPAT+Pandora%27s+Box")

    def test_string_with_non_replaceable_encoded_characters(self):
        self.assertEqual(TestReplaceValues.replacer.replace_values("12345%21%40%23%24%25%28%29"),
                         "12345%21%40%23%24%25%28%29")

    def test_string_with_repeated_values(self):
        self.assertEqual(TestReplaceValues.replacer.replace_values("Awp+Awp+Boom+Boom"), "AWP+AWP+BOOM+BOOM")

    def test_string_with_url_encoded_characters(self):
        self.assertEqual(TestReplaceValues.replacer.replace_values("Sticker+%7C+Art+%7C+Katowice+2019"),
                         "Sticker+%7C+arT+%7C+Katowice+2019")


class TestFetchData(unittest.TestCase):
    def test_fetch_data_skin(self):
        result = fetch_data("AWP+%7C+PAW+%28Factory+New%29")
        self.assertTrue(result['success'])

    def test_fetch_data_sticker(self):
        result = fetch_data("Sticker+%7C+RUSH+%7C+Cologne+2016")
        self.assertTrue(result['success'])

    def test_fetch_data_patch(self):
        result = fetch_data("Patch+%7C+MOUZ+%28Gold%29+%7C+Stockholm+2021")
        self.assertTrue(result['success'])

    def test_fetch_data_agent(self):
        result = fetch_data("Michael+Syfers++%7C+FBI+Sniper")
        self.assertTrue(result['success'])

    def test_music_kit_box(self):
        result = fetch_data("Tacticians+Music+Kit+Box")
        self.assertTrue(result['success'])

    def test_knife(self):
        result = fetch_data("%E2%98%85+Ursus+Knife+%7C+Doppler+%28Factory+New%29")
        self.assertTrue(result['success'])


class TestScraper(unittest.TestCase):

    def test_skin(self):
        pause_duration = 60

        normal_skin = Market_Scraper(
            "Black Lotus",
            weapon=CS2Weapon.M4A1S.value,
            quality=CS2Qualities.FACTORY_NEW.value)
        self.assertEqual(Market_Scraper(
            "Black Lotus",
            weapon=CS2Weapon.M4A1S.value,
            quality=CS2Qualities.FACTORY_NEW.value), normal_skin)

        stattrak_skin = Market_Scraper(
            "BOOM",
            weapon=CS2Weapon.AWP.value,
            quality=CS2Qualities.FIELD_TESTED.value,
            category=Category.STATTRAK.value)
        self.assertEqual(Market_Scraper(
            "BOOM", weapon=CS2Weapon.AWP.value,
            quality=CS2Qualities.FIELD_TESTED.value,
            category=Category.STATTRAK.value), stattrak_skin)

        souvenir_skin = Market_Scraper(
            "Chalice",
            weapon=CS2Weapon.CZ75_AUTO.value,
            quality=CS2Qualities.FACTORY_NEW.value,
            category=Category.SOUVENIR.value)
        self.assertEqual(Market_Scraper(
            "Chalice",
            weapon=CS2Weapon.CZ75_AUTO.value,
            quality=CS2Qualities.FACTORY_NEW.value,
            category=Category.SOUVENIR.value), souvenir_skin)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_patch(self):
        pause_duration = 60

        normal_patch = Market_Scraper(
            "El Pirata",
            category=Category.PATCH.value)
        self.assertEqual(Market_Scraper(
            "El Pirata",
            category=Category.PATCH.value), normal_patch)

        team_patch = Market_Scraper(
            "G2 Esports",
            category=Category.PATCH.value,
            major=Major.PGL_STOCKHOLM_2021.value)
        self.assertEqual(Market_Scraper(
            "G2 Esports",
            category=Category.PATCH.value,
            major=Major.PGL_STOCKHOLM_2021.value), team_patch)

        team_patch_with_quality = Market_Scraper(
            "Gambit Gaming",
            category=Category.PATCH.value,
            major=Major.PGL_STOCKHOLM_2021.value,
            quality=CS2Qualities.GOLD.value)
        self.assertEqual(Market_Scraper(
            "Gambit Gaming",
            category=Category.PATCH.value,
            major=Major.PGL_STOCKHOLM_2021.value,
            quality=CS2Qualities.GOLD.value), team_patch_with_quality)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_music_kit(self):
        pause_duration = 60

        normal_music_kit = Market_Scraper(
            "The Verkkars & n0thing, Flashbang Dance",
            category=Category.MUSIC_KIT.value)
        self.assertEqual(Market_Scraper(
            "The Verkkars & n0thing, Flashbang Dance",
            category=Category.MUSIC_KIT.value), normal_music_kit)

        stattrak_music_kit = Market_Scraper(
            "Scarlxrd, CHAIN$AW.LXADXUT.",
            category=Category.STATTRAK_MUSIC_KIT.value)
        self.assertEqual(Market_Scraper(
            "Scarlxrd, CHAIN$AW.LXADXUT.",
            category=Category.STATTRAK_MUSIC_KIT.value), stattrak_music_kit)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_music_kit_box(self):
        pause_duration = 60

        normal_music_kit_box = Market_Scraper(
            "Masterminds",
            category=Category.MUSIC_KIT_BOX.value)
        self.assertEqual(Market_Scraper(
            "Masterminds",
            category=Category.MUSIC_KIT_BOX.value), normal_music_kit_box)

        stattrak_music_kit_box = Market_Scraper(
            "Initiators",
            category=Category.STATTRAK_MUSIC_KIT_BOX.value)
        self.assertEqual(Market_Scraper(
            "Initiators",
            category=Category.STATTRAK_MUSIC_KIT_BOX.value), stattrak_music_kit_box)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_knife(self):
        pause_duration = 120

        normal_knife = Market_Scraper(
            "Tiger Tooth",
            weapon=CS2Weapon.TALON_KNIFE.value,
            quality=CS2Qualities.FACTORY_NEW.value,
            category=Category.KNIFE.value)
        self.assertEqual(Market_Scraper(
            "Tiger Tooth",
            weapon=CS2Weapon.TALON_KNIFE.value,
            quality=CS2Qualities.FACTORY_NEW.value,
            category=Category.KNIFE.value), normal_knife)

        stattrak_knife = Market_Scraper(
            "Tiger Tooth",
            weapon=CS2Weapon.TALON_KNIFE.value,
            quality=CS2Qualities.FACTORY_NEW.value,
            category=Category.STATTRAK_KNIFE.value)
        self.assertEqual(Market_Scraper(
            "Tiger Tooth",
            weapon=CS2Weapon.TALON_KNIFE.value,
            quality=CS2Qualities.FACTORY_NEW.value,
            category=Category.STATTRAK_KNIFE.value), stattrak_knife)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_sticker(self):
        pause_duration = 60

        normal_sticker = Market_Scraper(
            "Unicorn",
            category=Category.STICKER.value)
        self.assertEqual(Market_Scraper(
            "Unicorn",
            category=Category.STICKER.value), normal_sticker)

        autograph = Market_Scraper(
            "Spinx",
            category=Category.STICKER.value,
            quality=CS2Qualities.CHAMPION_GLITTER.value,
            major=Major.BLAST_TV_PARIS_2023.value)
        self.assertEqual(Market_Scraper(
            "Spinx",
            category=Category.STICKER.value,
            quality=CS2Qualities.CHAMPION_GLITTER.value,
            major=Major.BLAST_TV_PARIS_2023.value), autograph)

        team_sticker = Market_Scraper(
            "Vitality",
            category=Category.STICKER.value,
            quality=CS2Qualities.HOLO.value,
            major=Major.PGL_COPENHAGEN_2024.value)
        self.assertEqual(Market_Scraper(
            "Vitality",
            category=Category.STICKER.value,
            quality=CS2Qualities.HOLO.value,
            major=Major.PGL_COPENHAGEN_2024.value), team_sticker)

        sticker_with_quality = Market_Scraper(
            "Global TV",
            category=Category.STICKER.value,
            quality=CS2Qualities.LENTICULAR.value)
        self.assertEqual(Market_Scraper(
            "Global TV",
            category=Category.STICKER.value,
            quality=CS2Qualities.LENTICULAR.value), sticker_with_quality)

        sticker_without_price = Market_Scraper(
            "Titan",
            category=Category.STICKER.value, quality=CS2Qualities.HOLO.value)
        self.assertEqual(Market_Scraper(
            "Titan",
            category=Category.STICKER.value,
            quality=CS2Qualities.HOLO.value), sticker_without_price)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_sealed_graffiti(self):
        pause_duration = 60

        normal_sealed_graffiti = Market_Scraper(
            "Crown",
            category=Category.SEALED_GRAFFITI.value)
        self.assertEqual(Market_Scraper(
            "Crown",
            category=Category.SEALED_GRAFFITI.value), normal_sealed_graffiti)

        sealed_graffiti_with_quality = Market_Scraper(
            "Heart",
            category=Category.SEALED_GRAFFITI.value,
            quality=CS2Qualities.MONSTER_PURPLE.value)
        self.assertEqual(Market_Scraper(
            "Heart",
            category=Category.SEALED_GRAFFITI.value,
            quality=CS2Qualities.MONSTER_PURPLE.value), sealed_graffiti_with_quality)

        team_sealed_graffiti = Market_Scraper(
            "Tyloo",
            category=Category.SEALED_GRAFFITI.value,
            major=Major.FACEIT_LONDON_2018.value)
        self.assertEqual(Market_Scraper(
            "Tyloo",
            category=Category.SEALED_GRAFFITI.value,
            major=Major.FACEIT_LONDON_2018.value), team_sealed_graffiti)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_gloves(self):
        pause_duration = 60

        driver_gloves = Market_Scraper(
            "Queen Jaguar",
            category=Category.DRIVER_GLOVES.value,
            quality=CS2Qualities.FIELD_TESTED.value)
        self.assertEqual(Market_Scraper(
            "Queen Jaguar",
            category=Category.DRIVER_GLOVES.value,
            quality=CS2Qualities.FIELD_TESTED.value), driver_gloves)

        hydra_gloves = Market_Scraper(
            "Case Hardened",
            category=Category.HYDRA_GLOVES.value,
            quality=CS2Qualities.FACTORY_NEW.value)
        self.assertEqual(Market_Scraper(
            "Case Hardened",
            category=Category.HYDRA_GLOVES.value,
            quality=CS2Qualities.FACTORY_NEW.value), hydra_gloves)

        bloodhound_gloves = Market_Scraper(
            "Bronzed",
            category=Category.BLOODHOUND_GLOVES.value,
            quality=CS2Qualities.FIELD_TESTED.value)
        self.assertEqual(Market_Scraper(
            "Bronzed",
            category=Category.BLOODHOUND_GLOVES.value,
            quality=CS2Qualities.FIELD_TESTED.value), bloodhound_gloves)

        hand_wraps = Market_Scraper(
            "Cobalt Skulls",
            category=Category.HAND_WRAPS.value,
            quality=CS2Qualities.MINIMAL_WEAR.value)
        self.assertEqual(Market_Scraper(
            "Cobalt Skulls",
            category=Category.HAND_WRAPS.value,
            quality=CS2Qualities.MINIMAL_WEAR.value), hand_wraps)

        moto_gloves = Market_Scraper(
            "Finish Line",
            category=Category.MOTO_GLOVES.value,
            quality=CS2Qualities.MINIMAL_WEAR.value)
        self.assertEqual(Market_Scraper(
            "Finish Line",
            category=Category.MOTO_GLOVES.value,
            quality=CS2Qualities.MINIMAL_WEAR.value), moto_gloves)

        sport_gloves = Market_Scraper(
            "Amphibious",
            category=Category.SPORT_GLOVES.value,
            quality=CS2Qualities.FIELD_TESTED.value)
        self.assertEqual(Market_Scraper(
            "Amphibious",
            category=Category.SPORT_GLOVES.value,
            quality=CS2Qualities.FIELD_TESTED.value), sport_gloves)

        specialist_gloves = Market_Scraper(
            "Fade",
            category=Category.SPECIALIST_GLOVES.value,
            quality=CS2Qualities.FIELD_TESTED.value)
        self.assertEqual(Market_Scraper(
            "Fade",
            category=Category.SPECIALIST_GLOVES.value,
            quality=CS2Qualities.FIELD_TESTED.value), specialist_gloves)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_case(self):
        pause_duration = 60

        esports_2014_summer_case = Market_Scraper(
            "eSports 2014 Summer",
            category=Category.CASE.value)
        self.assertEqual(Market_Scraper(
            "eSports 2014 Summer",
            category=Category.CASE.value), esports_2014_summer_case)

        kilowatt_case = Market_Scraper(
            "Kilowatt",
            category=Category.CASE.value)
        self.assertEqual(Market_Scraper(
            "Kilowatt",
            category=Category.CASE.value), kilowatt_case)

        csgo_weapon_case = Market_Scraper(
            "CS:GO Weapon ",
            category=Category.CASE.value)
        self.assertEqual(Market_Scraper(
            "CS:GO Weapon ",
            category=Category.CASE.value), csgo_weapon_case)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_souvenir_package(self):
        pause_duration = 60

        rio_2022_inferno_souvenir_package = Market_Scraper(
            "Inferno",
            category=Category.SOUVENIR_PACKAGE.value,
            major=Major.IEM_RIO_2022.value)
        self.assertEqual(Market_Scraper(
            "Inferno",
            category=Category.SOUVENIR_PACKAGE.value,
            major=Major.IEM_RIO_2022.value), rio_2022_inferno_souvenir_package)

        stockholm_2021_overpass_souvenir_package = Market_Scraper(
            "Overpass",
            category=Category.SOUVENIR_PACKAGE.value,
            major=Major.PGL_STOCKHOLM_2021.value)
        self.assertEqual(Market_Scraper(
            "Overpass",
            category=Category.SOUVENIR_PACKAGE.value,
            major=Major.PGL_STOCKHOLM_2021.value), stockholm_2021_overpass_souvenir_package)

        copenhagen_2024_mirage_souvenir_package = Market_Scraper(
            "Mirage",
            category=Category.SOUVENIR_PACKAGE.value,
            major=Major.PGL_COPENHAGEN_2024.value)
        self.assertEqual(Market_Scraper(
            "Mirage",
            category=Category.SOUVENIR_PACKAGE.value,
            major=Major.PGL_COPENHAGEN_2024.value), copenhagen_2024_mirage_souvenir_package)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_pin(self):
        pause_duration = 60

        howl_pin = Market_Scraper(
            "Howl",
            category=Category.PIN.value)
        self.assertEqual(Market_Scraper(
            "Howl",
            category=Category.PIN.value), howl_pin)

        valeria_phoenix_pin = Market_Scraper(
            "Valeria Phoenix",
            category=Category.PIN.value)
        self.assertEqual(Market_Scraper(
            "Valeria Phoenix",
            category=Category.PIN.value), valeria_phoenix_pin)

        alyx_pin = Market_Scraper(
            "Alyx",
            category=Category.PIN.value)
        self.assertEqual(Market_Scraper(
            "Alyx",
            category=Category.PIN.value), alyx_pin)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_key(self):
        pause_duration = 60

        normal_key = Market_Scraper(
            "esports ",
            category=Category.CASE_KEY.value)
        self.assertEqual(Market_Scraper(
            "esports ",
            category=Category.CASE_KEY.value), normal_key)

        community_sticker_capsule_1_key = Market_Scraper(
            "Community Sticker Capsule 1",
            category=Category.CAPSULE_KEY.value)
        self.assertEqual(Market_Scraper(
            "Community Sticker Capsule 1",
            category=Category.CAPSULE_KEY.value), community_sticker_capsule_1_key)

        csgo_capsule_key = Market_Scraper(
            "CS:GO Capsule ",
            category=Category.CAPSULE_KEY.value)
        self.assertEqual(Market_Scraper(
            "CS:GO Capsule ",
            category=Category.CAPSULE_KEY.value), csgo_capsule_key)

        csgo_case_key = Market_Scraper(
            "CS:GO",
            category=Category.CASE_KEY.value)
        self.assertEqual(Market_Scraper(
            "CS:GO",
            category=Category.CASE_KEY.value), csgo_case_key)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_pass(self):
        pause_duration = 60

        normal_pass = Market_Scraper(
            "Operation Shattered Web Premium",
            category=Category.PASS.value)
        self.assertEqual(Market_Scraper(
            "Operation Shattered Web Premium",
            category=Category.PASS.value), normal_pass)

        normal_viewer_pass = Market_Scraper(
            "Copenhagen 2024",
            category=Category.VIEWER_PASS.value)
        self.assertEqual(Market_Scraper(
            "Copenhagen 2024",
            category=Category.VIEWER_PASS.value), normal_viewer_pass)

        viewer_pass_with_extra_tokens = Market_Scraper(
            "Antwerp 2022",
            category=Category.VIEWER_PASS_PLUS_3_TOKENS.value)
        self.assertEqual(Market_Scraper(
            "Antwerp 2022",
            category=Category.VIEWER_PASS_PLUS_3_TOKENS.value), viewer_pass_with_extra_tokens)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_agent(self):
        pause_duration = 60

        sir_bloody_miami_darryl = Market_Scraper(
            "Sir Bloody Miami Darryl",
            category=Category.AGENT.value,
            agent_type=CS2Agent.THE_PROFESSIONALS.value)
        self.assertEqual(Market_Scraper(
            "Sir Bloody Miami Darryl",
            category=Category.AGENT.value,
            agent_type=CS2Agent.THE_PROFESSIONALS.value), sir_bloody_miami_darryl)

        the_doctor_romanov = Market_Scraper(
            "'The Doctor' Romanov",
            category=Category.AGENT.value,
            agent_type=CS2Agent.SABRE.value)
        self.assertEqual(Market_Scraper(
            "'The Doctor' Romanov",
            category=Category.AGENT.value,
            agent_type=CS2Agent.SABRE.value), the_doctor_romanov)

        cmdr_mae_dead_cold_jamison = Market_Scraper(
            "Cmdr. Mae 'Dead Cold' Jamison",
            category=Category.AGENT.value,
            agent_type=CS2Agent.SWAT.value)
        self.assertEqual(Market_Scraper(
            "Cmdr. Mae 'Dead Cold' Jamison",
            category=Category.AGENT.value,
            agent_type=CS2Agent.SWAT.value), cmdr_mae_dead_cold_jamison)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_sticker_capsule(self):
        pause_duration = 60

        normal_sticker_capsule = Market_Scraper(
            "The Boardroom",
            category=Category.STICKER_CAPSULE.value)
        self.assertEqual(Market_Scraper(
            "The Boardroom",
            category=Category.STICKER_CAPSULE.value), normal_sticker_capsule)

        sticker_capsule_with_major = Market_Scraper(
            "Contenders",
            category=Category.STICKER_CAPSULE.value,
            major=Major.PGL_ANTWERP_2022)
        self.assertEqual(Market_Scraper(
            "Contenders",
            category=Category.STICKER_CAPSULE.value,
            major=Major.PGL_ANTWERP_2022), sticker_capsule_with_major)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_autograph_capsule(self):
        pause_duration = 60

        normal_autograph_capsule = Market_Scraper(
            "legends",
            category=Category.AUTOGRAPH_CAPSULE.value,
            major=Major.FACEIT_LONDON_2018.value)
        self.assertEqual(Market_Scraper(
            "legends",
            category=Category.AUTOGRAPH_CAPSULE.value,
            major=Major.FACEIT_LONDON_2018.value), normal_autograph_capsule)

        old_autograph_capsule = Market_Scraper(
            "Natus Vincere",
            category=Category.AUTOGRAPH_CAPSULE.value,
            major=Major.ESL_ONE_COLOGNE_2015.value)
        self.assertEqual(Market_Scraper(
            "Natus Vincere",
            category=Category.AUTOGRAPH_CAPSULE.value,
            major=Major.ESL_ONE_COLOGNE_2015.value), old_autograph_capsule)

        autograph_capsule_with_quality = Market_Scraper(
            "Challengers",
            category=Category.AUTOGRAPH_CAPSULE.value,
            major=Major.ELEAGUE_ATLANTA_2017.value,
            quality=CS2Qualities.FOIL.value)
        self.assertEqual(Market_Scraper(
            "Challengers",
            category=Category.AUTOGRAPH_CAPSULE.value,
            major=Major.ELEAGUE_ATLANTA_2017.value,
            quality=CS2Qualities.FOIL.value), autograph_capsule_with_quality)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

    def test_any(self):
        """
        Some items have specific name, so you should use ANY parameter to deal with it.
        Besides, you can use ANY parameter to search item using its full name
        :return:

        examples:
        """

        pause_duration = 60

        collectible_pins_capsule_series_1 = Market_Scraper(
            "Collectible Pins Capsule Series 1",
            category=Category.ANY.value)
        self.assertEqual(Market_Scraper(
            "Collectible Pins Capsule Series 1",
            category=Category.ANY.value), collectible_pins_capsule_series_1)

        community_sticker_capsule_1 = Market_Scraper(
            "Community Sticker Capsule 1",
            category=Category.ANY.value)
        self.assertEqual(Market_Scraper(
            "Community Sticker Capsule 1",
            category=Category.ANY.value), community_sticker_capsule_1)

        pallet_of_presents = Market_Scraper(
            "Pallet of Presents",
            category=Category.ANY.value)
        self.assertEqual(Market_Scraper(
            "Pallet of Presents",
            category=Category.ANY.value), pallet_of_presents)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

        audience_participation_parcel = Market_Scraper(
            "Audience Participation Parcel",
            category=Category.ANY.value)
        self.assertEqual(Market_Scraper(
            "Audience Participation Parcel",
            category=Category.ANY.value), audience_participation_parcel)

        gift_package = Market_Scraper(
            "Gift Package",
            category=Category.ANY.value)
        self.assertEqual(Market_Scraper(
            "Gift Package",
            category=Category.ANY.value), gift_package)

        name_tag = Market_Scraper(
            "Name Tag",
            category=Category.ANY.value)
        self.assertEqual(Market_Scraper(
            "Name Tag",
            category=Category.ANY.value), name_tag)

        stattrak_swap_tool = Market_Scraper(
            "StatTrak™ Swap Tool",
            category=Category.ANY.value)
        self.assertEqual(Market_Scraper(
            "StatTrak™ Swap Tool",
            category=Category.ANY.value), stattrak_swap_tool)

        csgo_graffiti_box = Market_Scraper(
            "CS:GO Graffiti Box",
            category=Category.ANY.value)
        self.assertEqual(Market_Scraper(
            "CS:GO Graffiti Box",
            category=Category.ANY.value), csgo_graffiti_box)

        csgo_patch_pack = Market_Scraper(
            "CS:GO Patch Pack",
            category=Category.ANY.value)
        self.assertEqual(Market_Scraper(
            "CS:GO Patch Pack",
            category=Category.ANY.value), csgo_patch_pack)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

        normal_skin = Market_Scraper(
            "AK-47 | Asiimov (Field-Tested)",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "AK-47 | Asiimov (Field-Tested)",
            category=Category.ANY.value
        ), normal_skin)

        normal_patch = Market_Scraper(
            "Patch | Copper Lambda",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Patch | Copper Lambda",
            category=Category.ANY.value
        ), normal_patch)

        normal_music_kit = Market_Scraper(
            "Music Kit | Sean Murray, A*D*8",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Music Kit | Sean Murray, A*D*8",
            category=Category.ANY.value
        ), normal_music_kit)

        normal_music_kit_box = Market_Scraper(
            "Initiators Music Kit Box",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Initiators Music Kit Box",
            category=Category.ANY.value
        ), normal_music_kit_box)

        normal_knife = Market_Scraper(
            "★ M9 Bayonet | Bright Water (Field-Tested)",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "★ M9 Bayonet | Bright Water (Field-Tested)",
            category=Category.ANY.value
        ), normal_knife)

        normal_sticker = Market_Scraper(
            "Sticker | Shifty Tactics",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Sticker | Shifty Tactics",
            category=Category.ANY.value
        ), normal_sticker)

        normal_sealed_graffiti = Market_Scraper(
            "Sealed Graffiti | EZ",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Sealed Graffiti | EZ",
            category=Category.ANY.value
        ), normal_sealed_graffiti)

        normal_gloves = Market_Scraper(
            "★ Hand Wraps | Spruce DDPAT (Battle-Scarred)",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "★ Hand Wraps | Spruce DDPAT (Battle-Scarred)",
            category=Category.ANY.value
        ), normal_gloves)

        normal_case = Market_Scraper(
            "Gamma 2 Case",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Gamma 2 Case",
            category=Category.ANY.value
        ), normal_case)

        print(f"pause {pause_duration} sec")
        time.sleep(pause_duration)

        normal_souvenir_package = Market_Scraper(
            "Cologne 2016 Mirage Souvenir Package",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Cologne 2016 Mirage Souvenir Package",
            category=Category.ANY.value
        ), normal_souvenir_package)

        normal_pin = Market_Scraper(
            "Baggage Pin",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Baggage Pin",
            category=Category.ANY.value
        ), normal_pin)

        normal_key = Market_Scraper(
            "Community Sticker Capsule 1 Key",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Community Sticker Capsule 1 Key",
            category=Category.ANY.value
        ), normal_key)

        normal_pass = Market_Scraper(
            "Operation Phoenix Pass",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Operation Phoenix Pass",
            category=Category.ANY.value
        ), normal_pass)

        normal_agent = Market_Scraper(
            "Sir Bloody Miami Darryl | The Professionals",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Sir Bloody Miami Darryl | The Professionals",
            category=Category.ANY.value
        ), normal_agent)

        normal_sticker_capsule = Market_Scraper(
            "Sticker Capsule",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Sticker Capsule",
            category=Category.ANY.value
        ), normal_sticker_capsule)

        normal_autograph_capsule = Market_Scraper(
            "Autograph Capsule | Astralis | Cologne 2016",
            category=Category.ANY.value
        )
        self.assertEqual(Market_Scraper(
            "Autograph Capsule | Astralis | Cologne 2016",
            category=Category.ANY.value
        ), normal_autograph_capsule)


if __name__ == '__main__':
    unittest.main()
