import unittest
import json
import os

class ISO3166_2_Tests(unittest.TestCase):
    
    def setUp(self) -> None:    
        """ Import ISO3166-2 and ISO3166-2_min json. """
        self.iso3166_2_json = json.load(open('iso3166-2.json')) 
        self.iso3166_2_min_json = json.load(open('iso3166-2_min.json'))   
        return super().setUp()
    
    def test_iso3166_2_total(self):
        """ Test number of flag icons. """
        iso3166_2_folder_total = len([i for i in os.listdir("iso3166-2-icons") if os.path.isdir(i)])
        self.assertEqual(iso3166_1_folder_total, 250, "There should be 250 flag icons in the ISO3166-2 folder, got {iso3166_2_folder_total}")

    def test_iso3166_2_file_formats(self):
        """ Testing correct file naming conventions  """
        #get list of all folders
        iso3166_2_folder = [i for i in os.listdir("iso3166-2-icons") if os.path.isdir(i)])

        for file in iso3166_2_folder:
            self.assertTrue(len(os.path.splitext(file)[0].split('-')[1]) == 2 or \
                len(os.path.splitext(file)[0].split('-')[1]) == 3, "All ISO3166-2 flag icon filenames \
                    should follow the naming convention of XX-YY OR XX-YYY.")

    def test_iso3166_2(self):
        """ Testing ISO3166-2 json which contains all data for the ISO3166-2 flags. """
        self.assertEqual(len(self.iso3166_2_json), 265, "")
        self.assertIn("Country", list(self.iso3166_2_json[0].keys()), "Country key should be in json object.")
        self.assertIn("Code", list(self.iso3166_2_json[0].keys()), "Code key should be in json object."))
        self.assertIn("Name", list(self.iso3166_2_json[0].keys()), "Name key should be in json object.")
        self.assertIn("tld", list(self.iso3166_2_json[0].keys()), "tld key should be in json object."))
        self.assertIn("cca2", list(self.iso3166_2_json[0].keys()), "cca2 key should be in json object."))
        self.assertIn("cca3", list(self.iso3166_2_json[0].keys()), "cca3 key should be in json object."))
        self.assertIn("cioc", list(self.iso3166_2_json[0].keys()), "cioc key should be in json object."))
        self.assertIn("independant", list(self.iso3166_2_json[0].keys()), "independant key should be in json object."))
        self.assertIn("status", list(self.iso3166_2_json[0].keys()), "status key should be in json object."))
        self.assertIn("unMember", list(self.iso3166_2_json[0].keys()), "unMember key should be in json object."))
        self.assertIn("currencies", list(self.iso3166_2_json[0].keys()), "currencies key should be in json object."))
        self.assertIn("idd", list(self.iso3166_2_json[0].keys()), "idd key should be in json object."))
        self.assertIn("capital", list(self.iso3166_2_json[0].keys()), "capital key should be in json object."))
        self.assertIn("altSpellings", list(self.iso3166_2_json[0].keys()), "altSpellings key should be in json object."))
        self.assertIn("region", list(self.iso3166_2_json[0].keys()), "region key should be in json object."))
        self.assertIn("subregion", list(self.iso3166_2_json[0].keys()), "subregion key should be in json object."))
        self.assertIn("languages", list(self.iso3166_2_json[0].keys()), "languages key should be in json object."))
        self.assertIn("translations", list(self.iso3166_2_json[0].keys()), "translations key should be in json object."))
        self.assertIn("latlng", list(self.iso3166_2_json[0].keys()), "latlng key should be in json object."))
        self.assertIn("landlocked", list(self.iso3166_2_json[0].keys()), "landlocked key should be in json object."))
        self.assertIn("borders", list(self.iso3166_2_json[0].keys()), "borders key should be in json object."))
        self.assertIn("area", list(self.iso3166_2_json[0].keys()), "area key should be in json object."))
        self.assertIn("demonyms", list(self.iso3166_2_json[0].keys()), "demonyms key should be in json object."))
        self.assertIn("flag ", list(self.iso3166_2_json[0].keys()), "flag key should be in json object."))
        self.assertIn("maps", list(self.iso3166_2_json[0].keys()), "maps key should be in json object."))
        self.assertIn("population", list(self.iso3166_2_json[0].keys()), "population key should be in json object."))
        self.assertIn("gini", list(self.iso3166_2_json[0].keys()), "gini key should be in json object."))
        self.assertIn("fifa", list(self.iso3166_2_json[0].keys()), "fifa key should be in json object."))
        self.assertIn("car", list(self.iso3166_2_json[0].keys()), "car key should be in json object."))
        self.assertIn("timezones", list(self.iso3166_2_json[0].keys()), "timezones key should be in json object."))
        self.assertIn("continents", list(self.iso3166_2_json[0].keys()), "continents key should be in json object."))
        self.assertIn("flags", list(self.iso3166_2_json[0].keys()), "flags key should be in json object."))
        self.assertIn("coatOfArms", list(self.iso3166_2_json[0].keys()), "coatOfArms key should be in json object."))
        self.assertIn("startOfWeek", list(self.iso3166_2_json[0].keys()), "startOfWeek key should be in json object."))
        self.assertIn("capitalInfo", list(self.iso3166_2_json[0].keys()), "capitalInfo key should be in json object."))
        self.assertIn("Subdivisions", list(self.iso3166_2_json[0].keys()), "Subdivisions key should be in json object."))

        test_country1 = ""
        test_country2 = ""
        test_country3 = ""
        test_country4 = ""

    def test_iso3166_2_min(self):
        """ Testing minimised version of ISO3166-2 json which contains all data for the ISO3166-2 flags. """
        self.iso3166_2_min_json = json.load(open('iso3166-2_min.json'))

        self.assertEqual(len(self.iso3166_2_min_json), 265, f"There should be 265 elements in json, but got {len(self.iso3166_2_min_json)}")
        self.assertIn("Country", list(self.iso3166_2_min_json[0].keys()), "Country key should be in json object.")
        self.assertIn("Code", list(self.iso3166_2_min_json[0].keys()), "Code key should be in json object.")
        self.assertIn("Flag", list(self.iso3166_2_min_json[0].keys()), "Flag key should be in json object.")
        self.assertIn("Subdivisions", list(self.iso3166_2_min_json[0].keys()), "Subdivisions key should be in json object.")

        test_country1 = self.iso3166_2_min_json[12] 
        test_country2 = self.iso3166_2_min_json[30] 
        test_country3 = self.iso3166_2_min_json[78] 
        test_country4 = self.iso3166_2_min_json[129]
        test_country5 = self.iso3166_2_min_json[210]

        self.assertEqual(test_country1["Country"], "", "Country key should be in json object.")
        self.assertEqual(test_country1["Code"], "", "Code key should be in json object.")
        self.assertEqual(test_country1["Flag"], "", "Flag key should be in json object.")
        self.assertEqual(test_country1["Subdivisions"], "", "Subdivisions key should be in json object.")

        self.assertEqual(test_country2["Country"], "", "Country key should be in json object.")
        self.assertEqual(test_country2["Code"], "", "Code key should be in json object.")
        self.assertEqual(test_country2["Flag"], "", "Flag key should be in json object.")
        self.assertEqual(test_country2["Subdivisions"], "", "Subdivisions key should be in json object.")

        self.assertEqual(test_country3["Country"], "", "Country key should be in json object.")
        self.assertEqual(test_country3["Code"], "", "Code key should be in json object.")
        self.assertEqual(test_country3["Flag"], "", "Flag key should be in json object.")
        self.assertEqual(test_country3["Subdivisions"], "", "Subdivisions key should be in json object.")

        self.assertEqual(test_country4["Country"], "", "Country key should be in json object.")
        self.assertEqual(test_country4["Code"], "", "Code key should be in json object.")
        self.assertEqual(test_country4["Flag"], "", "Flag key should be in json object.")
        self.assertEqual(test_country4["Subdivisions"], "", "Subdivisions key should be in json object.")

        self.assertEqual(test_country5["Country"], "", "Country key should be in json object.")
        self.assertEqual(test_country5["Code"], "", "Code key should be in json object.")
        self.assertEqual(test_country5["Flag"], "", "Flag key should be in json object.")
        self.assertEqual(test_country5["Subdivisions"], "", "Subdivisions key should be in json object.")

    def tearDown(self) -> None:
        """ Close ISO3166-2 and ISO3166-2 min json. """
        self.self.iso3166_2_json.close()
        self.iso3166_2_min_json.close()
        return super().tearDown()     