import unittest
import json
import os

class ISO3166_1Tests(unittest.TestCase):
    
    def setUp(self) -> None:      
        """ Import ISO3166-1 json. """
        self.iso3166_1_json = json.load(open('iso3166-1.json'))
        return super().setUp()
    
    def test_iso3166_1_length(self):
        """ Test number of flag icons. """
        iso3166_1_files_total = len([i for i in os.listdir("iso3166-1-icons") if os.path.isdir(i)])
        self.assertEqual(iso3166_1_files_total, 250, "There should be 250 flag icons in the ISO3166-1 folder, got {iso3166_1_files_total}")

    def test_iso3166_1_file_extensions(self):
        """ Test number of flag icons. """
        iso3166_1_files = [i for i in os.listdir("iso3166-1-icons") if i != "README.md"]
        for file in iso3166_1_files:
            self.assertTrue(os.path.splitext(file)[1] == ".svg", "All ISO3166-1 flag icons should be in the svg format.")

    def test_iso3166_1_file_formats(self):
        """ Testing correct file naming conventions  """
        #get list of all filenames, exclude UK and ES provincial flags
        iso3166_1_files = [i for i in os.listdir("iso3166-1-icons") \
            if (i != "README.md" or i != "gb-sct.svg" or i != "gb-nir.svg" or i != "gb-eng.svg" \
                or i != "es-ct.svg" or i != "es-ga.svg"]

        for file in iso3166_1_files:
            self.assertTrue(len(os.path.splitext(file)[0]) == 2, "All ISO3166-1 flag icon filenames should be 2 letters.")

    def test_iso3166_1(self):
        """ Testing ISO3166-1 json which contains all data for the ISO3166-1 flags. """
        self.assertEqual(len(iso3166_1_json), 265, "")
        self.assertIn("Country", list(self.iso3166_1_json[0].keys()), "")
        self.assertIn("Code", list(self.iso3166_1_json[0].keys()), "")
        self.assertIn("Flag", list(self.iso3166_1_json[0].keys()), "")

        br_test = self.iso3166_1_json[31]
        cp_test = self.iso3166_1_json[50]
        fr_test = self.iso3166_1_json[81]
        jm_test = self.iso3166_1_json[123]
        sv_test = self.iso3166_1_json[200]

        self.assertEqual(br_test['Country'], "Brazil", f"Test should return Brazil, got {br_test['Country']}")
        self.assertEqual(cp_test['Country'], "Clipperton Island", f"Test should return Clipperton Island, got {cp_test['Country']}")
        self.assertEqual(fr_test['Country'], "France", f"Test should return France, got {fr_test['Country']}")
        self.assertEqual(jm_test['Country'], "Jamaica", f"Test should return Jamaica, got {jm_test['Country']}")
        self.assertEqual(sv_test['Country'], "El Salvador", f"Test should return El Salvador, got {sv_test['Country']}")

        self.assertEqual(br_test['Code'], "BR", f"Test should return BR, got {br_test['Code']}")
        self.assertEqual(cp_test['Code'], "CP", f"Test should return CP, got {br_test['Code']}")
        self.assertEqual(fr_test['Code'], "FR", f"Test should return FR, got {br_test['Code']}")
        self.assertEqual(jm_test['Code'], "JM", f"Test should return JM, got {br_test['Code']}")
        self.assertEqual(sv_test['Code'], "SV", f"Test should return SV, got {br_test['Code']}")

        self.assertEqual(br_test['Flag'], '../iso3166-1-icons/br.svg', f"Test should return ../iso3166-1-icons/br.svg, got {br_test['Flag']}")
        self.assertEqual(cp_test['Flag'], '../iso3166-1-icons/cp.svg', f"Test should return ../iso3166-1-icons/cp.svg, got {br_test['Flag']}")
        self.assertEqual(fr_test['Flag'], '../iso3166-1-icons/fr.svg', f"Test should return ../iso3166-1-icons/fr.svg, got {br_test['Flag']}")
        self.assertEqual(jm_test['Flag'], '../iso3166-1-icons/jm.svg', f"Test should return ../iso3166-1-icons/jm.svg, got {br_test['Flag']}")
        self.assertEqual(sv_test['Flag'], '../iso3166-1-icons/sv.svg', f"Test should return ../iso3166-1-icons/sv.svg, got {br_test['Flag']}")

    def test_iso3166_files(self):
        """ Testing ISO3166-1 files. """
        iso3166_1_json = json.load(open('iso3166-1.json'))

        br_test = self.iso3166_1_json[31]
        cp_test = self.iso3166_1_json[50]
        fr_test = self.iso3166_1_json[81]
        jm_test = self.iso3166_1_json[123]
        sv_test = self.iso3166_1_json[200]
        sx_test = self.iso3166_1_json[222]

        self.assertTrue(os.path.isfile(br_test['Flag'], '../iso3166-1-icons/br.svg', f"br.svg should be a file in the ../iso3166-1-icons/ dir.")
        self.assertTrue(os.path.isfile(cp_test['Flag'], '../iso3166-1-icons/cp.svg', f"cp.svg should be a file in the ../iso3166-1-icons/ dir.")
        self.assertTrue(os.path.isfile(fr_test['Flag'], '../iso3166-1-icons/fr.svg', f"fr.svg should be a file in the ../iso3166-1-icons/ dir.")
        self.assertTrue(os.path.isfile(jm_test['Flag'], '../iso3166-1-icons/jm.svg', f"jm.svg should be a file in the ../iso3166-1-icons/ dir.")
        self.assertTrue(os.path.isfile(sv_test['Flag'], '../iso3166-1-icons/sv.svg', f"sv.svg should be a file in the ../iso3166-1-icons/ dir.")
        self.assertTrue(os.path.isfile(sx_test['Flag'], '../iso3166-1-icons/sx.svg', f"sx.svg should be a file in the ../iso3166-1-icons/ dir.")

    def tearDown(self) -> None:
        """ Close ISO3166-1 json. """
        self.iso3166_1_json.close()
        return super().tearDown()     

