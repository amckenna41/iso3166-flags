import unittest
import json
import os

class ISO3166_2_Tests(unittest.TestCase):
    
    def setUp(self) -> None:    
        """ Import ISO3166-2 and ISO3166-2_min json. """
        self.iso3166_2 = open(os.path.join('..', 'iso3166-2.json'))
        self.iso3166_2_json = json.load(self.iso3166_2)
        self.iso3166_2_min = open(os.path.join('..', 'iso3166-2_min.json'))
        self.iso3166_2_min_json = json.load(self.iso3166_2_min)   
        return super().setUp()
    
    def test_iso3166_2_total(self):
        """ Test number of flag icons. """
        iso3166_2_folder_total = len([i for i in os.listdir("../iso3166-2-icons") if os.path.isdir(os.path.join("../iso3166-2-icons", i))])
        self.assertEqual(iso3166_2_folder_total, 144, f"There should be 144 flag icons in the ISO3166-2 folder, got {iso3166_2_folder_total}")

    def test_iso3166_2_file_formats(self):
        """ Testing correct file naming conventions  """
        #get list of all folders
        iso3166_2_folder = [i for i in os.listdir("../iso3166-2-icons") if os.path.isdir(i)]

        for file in iso3166_2_folder:
            self.assertTrue(len(os.path.splitext(file)[0].split('-')[1]) == 2 or \
                len(os.path.splitext(file)[0].split('-')[1]) == 3, "All ISO3166-2 flag icon filenames \
                    should follow the naming convention of XX-YY OR XX-YYY.")
            self.assertTrue(os.path.splitext(file)[0].split('-')[0].isupper(), "All ISO3166-2 flag icon filenames \
                    should XX-YY OR XX-YYY and XX should be uppercase.")

            #if right-hand-side of ISO code is not numeric then check its uppercase
            if not (os.path.splitext(file)[0].split('-')[1].isnumeric()):
                self.assertTrue(os.path.splitext(file)[0].split('-')[1].isupper(), "All ISO3166-2 flag icon filenames \
                    should XX-YY OR XX-YYY and YY should be uppercase if it is not numeric.")

    def test_iso3166_2(self):
        """ Testing ISO3166-2 json which contains all data for the ISO3166-2 flags. """
        self.assertEqual(len(self.iso3166_2_json), 143, f"There should be 143 countries in the json, got {len(self.iso3166_2_json)}")
        self.assertIn("tld", list(self.iso3166_2_json[1].keys()), "tld key should be in json object.")
        self.assertIn("cca2", list(self.iso3166_2_json[1].keys()), "cca2 key should be in json object.")
        self.assertIn("cca3", list(self.iso3166_2_json[1].keys()), "cca3 key should be in json object.")
        self.assertIn("cioc", list(self.iso3166_2_json[1].keys()), "cioc key should be in json object.")
        self.assertIn("independent", list(self.iso3166_2_json[1].keys()), "independent key should be in json object.")
        self.assertIn("status", list(self.iso3166_2_json[1].keys()), "status key should be in json object.")
        self.assertIn("unMember", list(self.iso3166_2_json[1].keys()), "unMember key should be in json object.")
        self.assertIn("currencies", list(self.iso3166_2_json[1].keys()), "currencies key should be in json object.")
        self.assertIn("idd", list(self.iso3166_2_json[1].keys()), "idd key should be in json object.")
        self.assertIn("capital", list(self.iso3166_2_json[1].keys()), "capital key should be in json object.")
        self.assertIn("altSpellings", list(self.iso3166_2_json[1].keys()), "altSpellings key should be in json object.")
        self.assertIn("region", list(self.iso3166_2_json[1].keys()), "region key should be in json object.")
        self.assertIn("subregion", list(self.iso3166_2_json[1].keys()), "subregion key should be in json object.")
        self.assertIn("languages", list(self.iso3166_2_json[1].keys()), "languages key should be in json object.")
        self.assertIn("translations", list(self.iso3166_2_json[1].keys()), "translations key should be in json object.")
        self.assertIn("latlng", list(self.iso3166_2_json[1].keys()), "latlng key should be in json object.")
        self.assertIn("landlocked", list(self.iso3166_2_json[1].keys()), "landlocked key should be in json object.")
        self.assertIn("borders", list(self.iso3166_2_json[1].keys()), "borders key should be in json object.")
        self.assertIn("area", list(self.iso3166_2_json[1].keys()), "area key should be in json object.")
        self.assertIn("demonyms", list(self.iso3166_2_json[1].keys()), "demonyms key should be in json object.")
        self.assertIn("flag", list(self.iso3166_2_json[1].keys()), "flag key should be in json object.")
        self.assertIn("maps", list(self.iso3166_2_json[1].keys()), "maps key should be in json object.")
        self.assertIn("population", list(self.iso3166_2_json[1].keys()), "population key should be in json object.")
        self.assertIn("gini", list(self.iso3166_2_json[1].keys()), "gini key should be in json object.")
        self.assertIn("fifa", list(self.iso3166_2_json[1].keys()), "fifa key should be in json object.")
        self.assertIn("car", list(self.iso3166_2_json[1].keys()), "car key should be in json object.")
        self.assertIn("timezones", list(self.iso3166_2_json[1].keys()), "timezones key should be in json object.")
        self.assertIn("continents", list(self.iso3166_2_json[1].keys()), "continents key should be in json object.")
        self.assertIn("flags", list(self.iso3166_2_json[1].keys()), "flags key should be in json object.")
        self.assertIn("coatOfArms", list(self.iso3166_2_json[1].keys()), "coatOfArms key should be in json object.")
        self.assertIn("startOfWeek", list(self.iso3166_2_json[1].keys()), "startOfWeek key should be in json object.")
        self.assertIn("capitalInfo", list(self.iso3166_2_json[1].keys()), "capitalInfo key should be in json object.")
        self.assertIn("Subdivisions", list(self.iso3166_2_json[1].keys()), "Subdivisions key should be in json object.")

        test_country1 = self.iso3166_2_json[27] #CO
        test_country2 = self.iso3166_2_json[99] #PH
        test_country3 = self.iso3166_2_json[129] #UA
        test_country4 = self.iso3166_2_json[132] #US
        test_country5 = self.iso3166_2_json[141] #ZM

        self.assertEqual(test_country1["cca2"], "CO", f'Incorrect cca2 value, got {test_country1["cca2"]}, expected CO.')
        self.assertEqual(test_country1['capital'][0], "Bogotá", f'Incorrect capital value, got {test_country1["capital"][0]}, expected Bogotá.')
        self.assertEqual(int(test_country1['area']), 1141748, f'Incorrect area value, got {test_country1["area"]}, expected 1141748.')
        self.assertEqual(test_country1['gini'], {'2019': 51.3}, f'Incorrect gini value, got {test_country1["gini"]}, expected 2019: 51.3.')
        self.assertEqual(test_country1['continents'][0], "South America", f'Incorrect continents value, got {test_country1["continents"][0]}, expected South America.')

        self.assertEqual(test_country2["cca2"], "PH", f'Incorrect cca2 value, got {test_country2["cca2"]}, expected PH.')
        self.assertEqual(test_country2['capital'][0], "Manila", f'Incorrect capital value, got {test_country2["capital"][0]}, expected .')
        self.assertEqual(int(test_country2['area']), 342353, f'Incorrect area value, got {test_country2["area"]}, expected 342353.')
        self.assertEqual(test_country2['gini'], {'2018': 42.3}, f'Incorrect gini value, got {test_country2["gini"]}, expected 2018: 42.3.')
        self.assertEqual(test_country2['continents'][0], "Asia", f'Incorrect continents value, got {test_country2["continents"][0]}, expected Asia.')

        self.assertEqual(test_country3["cca2"], "UA", f'Incorrect cca2 value, got {test_country3["cca2"]}, expected UA.')
        self.assertEqual(test_country3['capital'][0], "Kyiv", f'Incorrect capital value, got {test_country1["capital"][0]}, expected Kyiv.')
        self.assertEqual(int(test_country3['area']), 603500, f'Incorrect area value, got {test_country3["area"]}, expected 603500.')
        self.assertEqual(test_country3['gini'], {'2019': 26.6}, f'Incorrect gini value, got {test_country3["gini"]}, expected 2019: 26.6.')
        self.assertEqual(test_country3['continents'][0], "Europe", f'Incorrect continents value, got {test_country3["continents"][0]}, expected Europe.')

        self.assertEqual(test_country4["cca2"], "US", f'Incorrect cca2 value, got {test_country4["cca2"]}, expected US.')
        self.assertEqual(test_country4['capital'][0], "Washington, D.C.", f'Incorrect capital value, got {test_country4["capital"][0]}, expected Washington, D.C.')
        self.assertEqual(test_country4['gini'], {'2018': 41.4}, f'Incorrect area value, got {test_country4["area"]}, expected 2018: 41.4.')
        self.assertEqual(int(test_country4['area']), 9372610, f'Incorrect gini value, got {test_country4["gini"]}, expected 9372610.')
        self.assertEqual(test_country4['continents'][0], "North America", f'Incorrect continents value, got {test_country4["continents"][0]}, expected North America.')

        self.assertEqual(test_country5["cca2"], "ZM", f'Incorrect cca2 value, got {test_country5["cca2"]}, expected ZM.')
        self.assertEqual(test_country5['capital'][0], "Lusaka", f'Incorrect capital value, got {test_country5["capital"][0]}, expected Lusaka.')
        self.assertEqual(test_country5['gini'], {'2015': 57.1}, f'Incorrect area value, got {test_country5["area"]}, expected 2015: 57.1.')
        self.assertEqual(int(test_country5['area']), 752612, f'Incorrect gini value, got {test_country5["gini"]}, expected 752612.')
        self.assertEqual(test_country5['continents'][0], "Africa", f'Incorrect continents value, got {test_country5["continents"][0]}, expected Africa.')

    def test_iso3166_2_min(self):
        """ Testing minimised version of ISO3166-2 json which contains all data for the ISO3166-2 flags. """
        self.assertEqual(len(self.iso3166_2_min_json), 143, f"There should be 143 elements in json, but got {len(self.iso3166_2_min_json)}")
        self.assertIn("Country", list(self.iso3166_2_min_json[0].keys()), "Country key should be in json object.")
        self.assertIn("Code", list(self.iso3166_2_min_json[0].keys()), "Code key should be in json object.")
        self.assertIn("Subdivisions", list(self.iso3166_2_min_json[0].keys()), "Subdivisions key should be in json object.")

        test_country1 = self.iso3166_2_min_json[12] #BG
        test_country2 = self.iso3166_2_min_json[30] #CV
        test_country3 = self.iso3166_2_min_json[78] #LY
        test_country4 = self.iso3166_2_min_json[126] #TR
        test_country5 = self.iso3166_2_min_json[142] #ZW

        self.assertEqual(test_country1["Country"], "Bulgaria", f'Country value incorrect, got {test_country1["Country"]}, expected Bulgaria.')
        self.assertEqual(test_country1["Code"], "BG", f'Code value incorrect, got {test_country1["Code"]}, expected BG.')
        self.assertEqual(len(test_country1["Subdivisions"]), 1, f'Incorrect number of subdivisionss, got {len(test_country1["Subdivisions"])}, expected 1.')
        self.assertEqual(test_country1["Subdivisions"]['BG-23'], "Sofia", f'Incorrect subdivision name, got {test_country1["Subdivisions"]["BG-23"]}, expected Sofia.')

        self.assertEqual(test_country2["Country"], "Cabo Verde", f'Country value incorrect, got {test_country2["Country"]}, expected Cabo Verde.')
        self.assertEqual(test_country2["Code"], "CV", f'Code value incorrect, got {test_country2["Code"]}, expected CV.')
        self.assertEqual(len(test_country2["Subdivisions"]), 4, f'Incorrect number of subdivisionss, got {len(test_country2["Subdivisions"])}, expected 4.')
        self.assertEqual(test_country2["Subdivisions"]['CV-MO'], "Mosteiros", f'Incorrect subdivision name, got {test_country2["Subdivisions"]["CV-MO"]}, expected Mosteiros.')
        self.assertEqual(test_country2["Subdivisions"]['CV-PR'], 'Praia', f'Incorrect subdivision name, got {test_country2["Subdivisions"]["CV-PR"]}, expected Praia.')
        self.assertEqual(test_country2["Subdivisions"]['CV-RB'], 'Ribeira Brava', f'Incorrect subdivision name, got {test_country2["Subdivisions"]["CV-RB"]}, expected Ribeira Brava.')
        self.assertEqual(test_country2["Subdivisions"]['CV-SM'], 'São Miguel', f'Incorrect subdivision name, got {test_country2["Subdivisions"]["CV-SM"]}, expected São Miguel.')

        self.assertEqual(test_country3["Country"], "Libya", f'Country value incorrect, got {test_country3["Country"]}, expected Libya.')
        self.assertEqual(test_country3["Code"], "LY", f'Code value incorrect, got {test_country3["Code"]}, expected LY.')
        self.assertEqual(len(test_country3["Subdivisions"]), 1, f'Incorrect number of subdivisionss, got {len(test_country3["Subdivisions"])}, expected 1.')
        self.assertEqual(test_country3["Subdivisions"]['LY-BA'], "Banghāzī", f'Incorrect subdivision name, got {test_country3["Subdivisions"]["LY-BA"]}, expected Banghāzī.')

        self.assertEqual(test_country4["Country"], "Turkey", f'Country value incorrect, got {test_country4["Country"]}, expected Turkey.')
        self.assertEqual(test_country4["Code"], "TR", f'Code value incorrect, got {test_country4["Code"]}, expected TR.')
        self.assertEqual(len(test_country4["Subdivisions"]), 3, f'Incorrect number of subdivisionss, got {len(test_country4["Subdivisions"])}, expected 3.')
        self.assertEqual(test_country4["Subdivisions"]['TR-34'], "İstanbul", f'Incorrect subdivision name, got {test_country4["Subdivisions"]["TR-34"]}, expected İstanbul.')
        self.assertEqual(test_country4["Subdivisions"]['TR-48'], "Muğla", f'Incorrect subdivision name, got {test_country4["Subdivisions"]["TR-48"]}, expected Muğla.')
        self.assertEqual(test_country4["Subdivisions"]['TR-54'], "Sakarya", f'Incorrect subdivision name, got {test_country4["Subdivisions"]["TR-54"]}, expected Sakarya.')

        self.assertEqual(test_country5["Country"], "Zimbabwe", f'Country value incorrect, got {test_country5["Country"]}, expected Zimbabwe.')
        self.assertEqual(test_country5["Code"], "ZW", f'Code value incorrect, got {test_country5["Code"]}, expected ZW.')
        self.assertEqual(len(test_country5["Subdivisions"]), 2, f'Incorrect number of subdivisionss, got {len(test_country5["Subdivisions"])}, expected 2.')
        self.assertEqual(test_country5["Subdivisions"]['ZW-BU'], "Bulawayo", f'Incorrect subdivision name, got {test_country5["Subdivisions"]["ZW-BU"]}, expected Bulawayo.')
        self.assertEqual(test_country5["Subdivisions"]['ZW-HA'], "Harare", f'Incorrect subdivision name, got {test_country5["Subdivisions"]["ZW-HA"]}, expected Harare.')

        with(self.assertRaises(TypeError, msg="Key Error raised, invalid data type.")):
            test_country = self.iso3166_2_min_json["ABC"]

        with(self.assertRaises(IndexError, msg="Index Error raised, invalid data index for json.")):
            test_country = self.iso3166_2_min_json[300]
        
    def tearDown(self) -> None:
        """ Delete ISO3166-2 and ISO3166-2 min json objects. """
        self.iso3166_2.close() 
        self.iso3166_2_min.close() 
        del self.iso3166_2_json
        del self.iso3166_2_min_json
        return super().tearDown()     

if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()