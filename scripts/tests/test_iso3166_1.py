import unittest
import json
import os

class ISO3166_1Tests(unittest.TestCase):
    """
    
    """
    def setUp(self) -> None:      
        """ Import ISO3166-1 json. """
        self.iso3166_1_dir = os.path.join("..", "iso3166-1-icons")
        self.iso3166_1 = open(os.path.join('..', 'iso3166-1.json'))
        self.iso3166_1_json = json.load(self.iso3166_1)
        return super().setUp()
    
    def test_iso3166_1_length(self):
        """ Test number of flag icons. """
        iso3166_1_files_total = len([i for i in os.listdir(self.iso3166_1_dir) if os.path.isfile(os.path.join(self.iso3166_1_dir, i))])
        self.assertEqual(iso3166_1_files_total, 265, "There should be 265 flag icons in the ISO3166-1 folder, got {iso3166_1_files_total}.")

    def test_iso3166_1_file_extensions(self):
        """ Test file extensions for all flags. """
        iso3166_1_files = [i for i in os.listdir(self.iso3166_1_dir) if i != "README.md" and i != ".DS_Store"]
        for file in iso3166_1_files:
            self.assertTrue(os.path.splitext(file)[1] == ".svg", "All ISO3166-1 flag icons should be in the svg format.")

    def test_iso3166_1_file_formats(self):
        """ Testing correct file naming conventions  """
        #get list of all filenames, exclude UK, ES provincial flags and readme
        iso3166_1_files = [i for i in os.listdir(self.iso3166_1_dir) \
            if (i != "README.md" and i != ".DS_Store" and i != "gb-sct.svg" \
                and i != "gb-nir.svg" and i != "gb-eng.svg" and i != "gb-wls.svg" \
                    and i != "es-ct.svg" and i != "es-ga.svg")]

        for file in iso3166_1_files:
            self.assertTrue(len(os.path.splitext(file)[0]) == 2, "All ISO3166-1 flag icon filenames should be 2 letters.")
            self.assertTrue(file.islower(), 'All ISO3166-1 flag icon filenames should be in lower-case.')
        
    def test_iso3166_1(self):
        """ Testing ISO3166-1 json which contains all data for the ISO3166-1 flags. """
        self.assertEqual(len(self.iso3166_1_json), 265, "")
        self.assertIn("Country", list(self.iso3166_1_json[0].keys()), "")
        self.assertIn("Code", list(self.iso3166_1_json[0].keys()), "")
        self.assertIn("Flag", list(self.iso3166_1_json[0].keys()), "")

        br_test = self.iso3166_1_json[31]
        cp_test = self.iso3166_1_json[50]
        fr_test = self.iso3166_1_json[81]
        jm_test = self.iso3166_1_json[123]
        ro_test = self.iso3166_1_json[200]
        tg_test = self.iso3166_1_json[229]

        self.assertEqual(br_test['Country'], "Brazil", f"Test should return Brazil, got {br_test['Country']}")
        self.assertEqual(cp_test['Country'], "Clipperton Island", f"Test should return Clipperton Island, got {cp_test['Country']}")
        self.assertEqual(fr_test['Country'], "France", f"Test should return France, got {fr_test['Country']}")
        self.assertEqual(jm_test['Country'], "Jamaica", f"Test should return Jamaica, got {jm_test['Country']}")
        self.assertEqual(ro_test['Country'], "Romania", f"Test should return Romania, got {ro_test['Country']}")
        self.assertEqual(tg_test['Country'], "Togo", f"Test should return Togo, got {tg_test['Country']}")

        self.assertEqual(br_test['Code'], "BR", f"Test should return BR, got {br_test['Code']}")
        self.assertEqual(cp_test['Code'], "CP", f"Test should return CP, got {cp_test['Code']}")
        self.assertEqual(fr_test['Code'], "FR", f"Test should return FR, got {fr_test['Code']}")
        self.assertEqual(jm_test['Code'], "JM", f"Test should return JM, got {jm_test['Code']}")
        self.assertEqual(ro_test['Code'], "RO", f"Test should return RO, got {ro_test['Code']}")
        self.assertEqual(tg_test['Code'], "TG", f"Test should return TG, got {tg_test['Code']}")

        self.assertEqual(br_test['Flag'], '../iso3166-1-icons/br.svg', f"Test should return ../iso3166-1-icons/br.svg, got {br_test['Flag']}")
        self.assertEqual(cp_test['Flag'], '../iso3166-1-icons/cp.svg', f"Test should return ../iso3166-1-icons/cp.svg, got {cp_test['Flag']}")
        self.assertEqual(fr_test['Flag'], '../iso3166-1-icons/fr.svg', f"Test should return ../iso3166-1-icons/fr.svg, got {fr_test['Flag']}")
        self.assertEqual(jm_test['Flag'], '../iso3166-1-icons/jm.svg', f"Test should return ../iso3166-1-icons/jm.svg, got {jm_test['Flag']}")
        self.assertEqual(ro_test['Flag'], '../iso3166-1-icons/ro.svg', f"Test should return ../iso3166-1-icons/ro.svg, got {ro_test['Flag']}")
        self.assertEqual(tg_test['Flag'], '../iso3166-1-icons/tg.svg', f"Test should return ../iso3166-1-icons/tg.svg, got {tg_test['Flag']}")

    def test_iso3166_files(self):
        """ Testing ISO3166-1 files. """
        br_test = self.iso3166_1_json[31]
        cp_test = self.iso3166_1_json[50]
        fr_test = self.iso3166_1_json[81]
        jm_test = self.iso3166_1_json[123]
        ro_test = self.iso3166_1_json[200]
        tg_test = self.iso3166_1_json[222]

        self.assertTrue(os.path.isfile(br_test['Flag']), f"br.svg should be a file in the ../iso3166-1-icons/ dir.")
        self.assertTrue(os.path.isfile(cp_test['Flag']), f"cp.svg should be a file in the ../iso3166-1-icons/ dir.")
        self.assertTrue(os.path.isfile(fr_test['Flag']), f"fr.svg should be a file in the ../iso3166-1-icons/ dir.")
        self.assertTrue(os.path.isfile(jm_test['Flag']), f"jm.svg should be a file in the ../iso3166-1-icons/ dir.")
        self.assertTrue(os.path.isfile(ro_test['Flag']), f"ro.svg should be a file in the ../iso3166-1-icons/ dir.")
        self.assertTrue(os.path.isfile(tg_test['Flag']), f"tg.svg should be a file in the ../iso3166-1-icons/ dir.")

    def tearDown(self) -> None:
        """ Delete ISO3166-1 json object. """
        self.iso3166_1.close()
        del self.iso3166_1_json
        return super().tearDown()     

if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()