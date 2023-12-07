import unittest
import json
import os
import pycountry

class ISO3166_2_Tests(unittest.TestCase):
    """
    Unit tests for the iso3166-2-icons directory which tests the correct total number
    of files, correct file naming conventions, duplicate files, correct file
    extensions and the various keys and values of the 2 ISO3166-2 json files
    in the repo (iso3166-2.json & iso3166-2-min.json)

    """
    def setUp(self) -> None:    
        """ Import ISO3166-2 and ISO3166-2_min json. """
        self.iso3166_2_folder = "../iso3166-2-icons"
        self.iso3166_2 = open(os.path.join('..', 'iso3166-2.json'))
        self.iso3166_2_json = json.load(self.iso3166_2)
        self.iso3166_2_min = open(os.path.join('..', 'iso3166-2-min.json'))
        self.iso3166_2_min_json = json.load(self.iso3166_2_min)   
        return super().setUp()
    
    def test_iso3166_2_total(self):
        """ Test number of flag icons. """
        iso3166_2_folder_total = len([i for i in os.listdir(self.iso3166_2_folder) if os.path.isdir(os.path.join(self.iso3166_2_folder, i))])
        self.assertEqual(iso3166_2_folder_total, 148, f"There should be 148 flag icon folders in the ISO3166-2 folder, got {iso3166_2_folder_total}")

    def test_iso3166_2_file_naming(self):
        """ Testing correct file naming conventions. """
        #get list of all folders
        iso3166_2_folder = [i for i in os.listdir(self.iso3166_2_folder) if os.path.isdir(os.path.join(self.iso3166_2_folder, i))]

        for folder in iso3166_2_folder:
            #get list of files in country folder
            iso3166_2_files = [i for i in os.listdir(os.path.join(self.iso3166_2_folder, folder)) if os.path.isfile(os.path.join(self.iso3166_2_folder, folder, i))]
            iso3166_2_files.sort()

            #remove any unneeded files for testing
            if ("README.md") in iso3166_2_files:
                iso3166_2_files.remove("README.md")
            if (".DS_Store") in iso3166_2_files:
                iso3166_2_files.remove(".DS_Store")

            #get sorted list of a country's subdivision codes
            allSubdivs = []
            for subd in pycountry.subdivisions.get(country_code=folder): allSubdivs.append(subd.code)
            allSubdivs.sort()

            #iterate over all files and test correct naming conventions
            for file in iso3166_2_files:
                
                invalids = ["GT", "LV", "RS", "PA", "CD", "FR", "IQ", "ET", "GB"] #skip these for now

                if (folder not in invalids): #skipping invalid codes as subdivisions in pycountry module are incorrect
                    #test filename is valid country subdivision
                    self.assertIn(os.path.splitext(file)[0], allSubdivs, f'Filename is not a valid ISO3166-2 subdivision for {folder}: {file}')

                #test LHS of filename is 2 chars in length
                self.assertTrue(len(file.split('-')[0]) == 2, \
                    f"All ISO3166-2 flag icon filenames should follow the naming convention of XX-YY OR XX-YYY: {file}.")
                
                #test RHS of filename is of length 1, 2 or 3
                self.assertTrue((len(file.split('-')[1].split('.')[0]) <= 3), \
                    f"All ISO3166-2 flag icon filenames should follow the naming convention of XX-YY OR XX-YYY: {file}.")

                #test LHS of filename is uppercase
                self.assertTrue(file.split('-')[0].split('.')[0].isupper(), \
                    f"All ISO3166-2 flag icon filenames should follow the naming convention of XX-YY OR XX-YYY, where XX is uppercase: {file}.")

                #if right-hand-side of ISO code is not numeric then check its uppercase
                if not (file.split('-')[1].split('.')[0].isnumeric()):
                    self.assertTrue(file.split('-')[1].split('.')[0].isupper(),
                        f"All ISO3166-2 flag icon filenames should follow the naming convention of XX-YY OR XX-YYY: {file}.")
    
    def test_iso311_2_file_duplicates(self):
        """ Testing only one version of flag exists, regardless of file format. """
        #get list of all folders
        iso3166_2_folder = [i for i in os.listdir(self.iso3166_2_folder) if os.path.isdir(os.path.join(self.iso3166_2_folder, i))]
        allFiles = []

        for folder in iso3166_2_folder:
            #get sorted list of files in country folder
            iso3166_2_files = [i for i in os.listdir(os.path.join(self.iso3166_2_folder, folder)) if os.path.isfile(os.path.join(self.iso3166_2_folder, folder, i))]
            iso3166_2_files.sort()

            #remove any unneeded files for testing
            if ("README.md") in iso3166_2_files:
                iso3166_2_files.remove("README.md")
            if (".DS_Store") in iso3166_2_files:
                iso3166_2_files.remove(".DS_Store")

            #get list of a folder's file extensions
            iso3166_2_files = list(map(lambda f: os.path.splitext(f)[0], iso3166_2_files))
            duplicate_index = 0
            if (len(iso3166_2_files) != len(set(iso3166_2_files))):
                duplicate_index = [idx for idx, item in enumerate(iso3166_2_files) if item in iso3166_2_files[:idx]][0]

            #test only 1 version of flag is in folder, regardless of file extension
            self.assertEqual(len(iso3166_2_files), len(set(iso3166_2_files)), \
                f"All ISO3166-2 flag icon filenames must be unique, regardless of file extension, duplicate filename: {iso3166_2_files[duplicate_index]}.")

    def test_iso3166_2_extensions(self):
        """ Testing correct file extensions. """
        #get list of all folders
        iso3166_2_folder = [i for i in os.listdir(self.iso3166_2_folder) if os.path.isdir(os.path.join(self.iso3166_2_folder, i))]
        valid_extensions = [".svg", ".png", ".jpg", ".jpeg", ".gif"]

        for folder in iso3166_2_folder:
            #get list of files in country folder
            iso3166_2_files = [i for i in os.listdir(os.path.join(self.iso3166_2_folder, folder)) if os.path.isfile(os.path.join(self.iso3166_2_folder, folder, i))]
            #remove any unneeded files for testing
            if ("README.md") in iso3166_2_files:
                iso3166_2_files.remove("README.md")
            if (".DS_Store") in iso3166_2_files:
                iso3166_2_files.remove(".DS_Store")

            #get list of a folder's file extensions
            iso3166_2_files = list(map(lambda f: os.path.splitext(f)[1], iso3166_2_files))

            #iterate over all files and test correct file extensions
            for file in iso3166_2_files:
                #test file extension is valid
                self.assertTrue(file in valid_extensions, \
                    f"All ISO3166-2 flag icon filenames should be svg, png, jpg, jpeg or gif: {file}")

    def test_iso3166_2(self):
        """ Testing ISO3166-2 json which contains all data for the ISO3166-2 flags. """
        self.assertEqual(len(self.iso3166_2_json), 148, f"There should be 148 countries in the json, got {len(self.iso3166_2_json)}")
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

        test_country1 = self.iso3166_2_json[28] #CR
        test_country2 = self.iso3166_2_json[100] #PA
        test_country3 = self.iso3166_2_json[131] #TR
        test_country4 = self.iso3166_2_json[134] #UA
        test_country5 = self.iso3166_2_json[145] #ZA

        self.assertEqual(test_country1["cca2"], "CR", f'Incorrect cca2 value, got {test_country1["cca2"]}, expected CR.')
        self.assertEqual(test_country1['capital'][0], "San José", f'Incorrect capital value, got {test_country1["capital"][0]}, expected San José.')
        self.assertEqual(int(test_country1['area']), 51100, f'Incorrect area value, got {test_country1["area"]}, expected 51100.')
        self.assertEqual(test_country1['gini'], {'2019': 48.2}, f'Incorrect gini value, got {test_country1["gini"]}, expected 2019: 48.2.')
        self.assertEqual(test_country1['continents'][0], "North America", f'Incorrect continents value, got {test_country1["continents"][0]}, expected North America.')

        self.assertEqual(test_country2["cca2"], "PA", f'Incorrect cca2 value, got {test_country2["cca2"]}, expected PA.')
        self.assertEqual(test_country2['capital'][0], "Panama City", f'Incorrect capital value, got {test_country2["capital"][0]}, Panama City.')
        self.assertEqual(int(test_country2['area']), 75417, f'Incorrect area value, got {test_country2["area"]}, expected 75417.')
        self.assertEqual(test_country2['gini'], {'2019': 49.8}, f'Incorrect gini value, got {test_country2["gini"]}, expected 2018: 49.8.')
        self.assertEqual(test_country2['continents'][0], "North America", f'Incorrect continents value, got {test_country2["continents"][0]}, expected North America.')

        self.assertEqual(test_country3['capital'][0], "Ankara", f'Incorrect capital value, got {test_country1["capital"][0]}, expected Ankara.')
        self.assertEqual(int(test_country3['area']), 783562, f'Incorrect area value, got {test_country3["area"]}, expected 783562.')
        self.assertEqual(test_country3['gini'], {'2019': 41.9}, f'Incorrect gini value, got {test_country3["gini"]}, expected 2019: 26.6.')
        self.assertEqual(test_country3['continents'][0], "Asia", f'Incorrect continents value, got {test_country3["continents"][0]}, expected Asia.')

        self.assertEqual(test_country4["cca2"], "UA", f'Incorrect cca2 value, got {test_country4["cca2"]}, expected UA.')
        self.assertEqual(test_country4['capital'][0], "Kyiv", f'Incorrect capital value, got {test_country4["capital"][0]}, expected Kyiv.')
        self.assertEqual(test_country4['gini'], {'2019': 26.6}, f'Incorrect area value, got {test_country4["area"]}, expected 2018: 41.4.')
        self.assertEqual(int(test_country4['area']), 603500, f'Incorrect gini value, got {test_country4["gini"]}, expected 603500.')
        self.assertEqual(test_country4['continents'][0], "Europe", f'Incorrect continents value, got {test_country4["continents"][0]}, expected Europe.')

        self.assertEqual(test_country5["cca2"], "ZA", f'Incorrect cca2 value, got {test_country5["cca2"]}, expected ZA.')
        self.assertEqual(test_country5['capital'][0], "Pretoria", f'Incorrect capital value, got {test_country5["capital"][0]}, expected Pretoria.')
        self.assertEqual(test_country5['gini'], {'2014': 63.0}, f'Incorrect area value, got {test_country5["area"]}, expected 2015: 57.1.')
        self.assertEqual(int(test_country5['area']), 1221037, f'Incorrect gini value, got {test_country5["gini"]}, expected 1221037.')
        self.assertEqual(test_country5['continents'][0], "Africa", f'Incorrect continents value, got {test_country5["continents"][0]}, expected Africa.')

    def test_iso3166_2_min(self):
        """ Testing minimised version of ISO3166-2 json which contains all data for the ISO3166-2 flags. """
        self.assertEqual(len(self.iso3166_2_min_json), 148, f"There should be 148 elements in json, but got {len(self.iso3166_2_min_json)}")
        self.assertIn("Country", list(self.iso3166_2_min_json[0].keys()), "Country key should be in json object.")
        self.assertIn("Code", list(self.iso3166_2_min_json[0].keys()), "Code key should be in json object.")
        self.assertIn("Subdivisions", list(self.iso3166_2_min_json[0].keys()), "Subdivisions key should be in json object.")

        test_country1 = self.iso3166_2_min_json[12] #BG
        test_country2 = self.iso3166_2_min_json[30] #CV
        test_country3 = self.iso3166_2_min_json[78] #LU
        test_country4 = self.iso3166_2_min_json[125] #ST
        test_country5 = self.iso3166_2_min_json[144] #YE

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

        self.assertEqual(test_country3["Country"], "Luxembourg", f'Country value incorrect, got {test_country3["Country"]}, expected Luxembourg.')
        self.assertEqual(test_country3["Code"], "LU", f'Code value incorrect, got {test_country3["Code"]}, expected LU.')
        self.assertEqual(len(test_country3["Subdivisions"]), 12, f'Incorrect number of subdivisionss, got {len(test_country3["Subdivisions"])}, expected 12.')
        self.assertEqual(test_country3["Subdivisions"]['LU-CA'], "Capellen", f'Incorrect subdivision name, got {test_country3["Subdivisions"]["LU-CA"]}, expected Capellen.')
        self.assertEqual(test_country3["Subdivisions"]['LU-GR'], "Grevenmacher", f'Incorrect subdivision name, got {test_country3["Subdivisions"]["LU-GR"]}, expected Grevenmacher.')
        self.assertEqual(test_country3["Subdivisions"]['LU-RM'], "Remich", f'Incorrect subdivision name, got {test_country3["Subdivisions"]["LU-RM"]}, expected Remich.')

        self.assertEqual(test_country4["Country"], "Sao Tome and Principe", f'Country value incorrect, got {test_country4["Country"]}, expected Sao Tome and Principe.')
        self.assertEqual(test_country4["Code"], "ST", f'Code value incorrect, got {test_country4["Code"]}, expected ST.')
        self.assertEqual(len(test_country4["Subdivisions"]), 2, f'Incorrect number of subdivisionss, got {len(test_country4["Subdivisions"])}, expected 2.')
        self.assertEqual(test_country4["Subdivisions"]['ST-01'], "Água Grande", f'Incorrect subdivision name, got {test_country4["Subdivisions"]["ST-01"]}, expected Água Grande.')
        self.assertEqual(test_country4["Subdivisions"]['ST-P'], "Príncipe", f'Incorrect subdivision name, got {test_country4["Subdivisions"]["ST-P"]}, expected Príncipe.')

        self.assertEqual(test_country5["Country"], "Yemen", f'Country value incorrect, got {test_country5["Country"]}, expected Yemen.')
        self.assertEqual(test_country5["Code"], "YE", f'Code value incorrect, got {test_country5["Code"]}, expected YE.')
        self.assertEqual(len(test_country5["Subdivisions"]), 4, f'Incorrect number of subdivisionss, got {len(test_country5["Subdivisions"])}, expected 4.')
        self.assertEqual(test_country5["Subdivisions"]['YE-AD'], "‘Adan", f'Incorrect subdivision name, got {test_country5["Subdivisions"]["YE-AD"]}, expected ‘Adan.')
        self.assertEqual(test_country5["Subdivisions"]['YE-DH'], "Dhamār", f'Incorrect subdivision name, got {test_country5["Subdivisions"]["YE-DH"]}, expected Dhamār.')
        self.assertEqual(test_country5["Subdivisions"]['YE-HD'], "Ḩaḑramawt", f'Incorrect subdivision name, got {test_country5["Subdivisions"]["YE-HD"]}, expected Ḩaḑramawt.')
        self.assertEqual(test_country5["Subdivisions"]['YE-LA'], "Laḩij", f'Incorrect subdivision name, got {test_country5["Subdivisions"]["YE-LA"]}, expected Laḩij.')


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