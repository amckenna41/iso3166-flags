import os
import re
import sys
import argparse
from lxml import etree
from iso3166_2 import Subdivisions

#no external entities/network access - flags come from upstream syncs and contributors
SAFE_XML_PARSER = etree.XMLParser(resolve_entities="internal", no_network=True)

#script URLs, and references that make the browser fetch a remote resource (http(s):// or protocol-relative //)
SCRIPT_URL = re.compile(r"^\s*(javascript|vbscript):", re.IGNORECASE)
REMOTE_URL = re.compile(r"^\s*(https?:)?//", re.IGNORECASE)
CSS_REMOTE_URL = re.compile(r"url\(\s*['\"]?\s*((https?:)?//|javascript:)|@import", re.IGNORECASE)

FLAG_EXTENSIONS = (".svg", ".png", ".jpg", ".jpeg")
IGNORED_FILES = {"README.md", ".DS_Store"}

def check_svg_safety(svg_path: str) -> list:
    """
    Check an SVG flag for content that would run script or fetch remote resources once the SVG is inlined
    into a page (e.g via the iso3166-1 sprite): <script> elements, on* event handler attributes,
    javascript:/vbscript: URLs and remote http(s):// references in hrefs or CSS.

    Parameters
    ==========
    :svg_path: str
        path to the SVG file.

    Returns
    =======
    :errors: list
        list of human-readable problems found, empty if the SVG is safe.
    """
    try:
        root = etree.parse(svg_path, SAFE_XML_PARSER).getroot()  # nosec B320
    except etree.XMLSyntaxError as e:
        return [f"{svg_path}: invalid XML ({e})"]

    errors = []
    for el in root.iter():
        #skip comments and processing instructions
        if not isinstance(el.tag, str):
            continue
        tag = etree.QName(el).localname
        if tag == "script":
            errors.append(f"{svg_path}: <script> element")
        #CSS inside <style> blocks
        if tag == "style" and el.text and CSS_REMOTE_URL.search(el.text):
            errors.append(f"{svg_path}: remote url/@import in <style>")
        for attr, value in el.attrib.items():
            name = etree.QName(attr).localname
            if name.lower().startswith("on"):
                errors.append(f"{svg_path}: event handler attribute {name} on <{tag}>")
            elif SCRIPT_URL.search(value):
                errors.append(f"{svg_path}: script URL in {name} on <{tag}>")
            elif name == "href" and REMOTE_URL.search(value):
                errors.append(f"{svg_path}: remote href {value.strip()[:60]} on <{tag}>")
            elif name == "style" and CSS_REMOTE_URL.search(value):
                errors.append(f"{svg_path}: remote url in style on <{tag}>")
    return errors

def check_iso3166_2_filenames(iso3166_2_dir: str="iso3166-2-flags", subdivisions: Subdivisions=None) -> list:
    """
    Check every file in the ISO 3166-2 flag folder is a supported flag format, sits in a valid
    ISO 3166-1 alpha-2 country sub-folder and is named after a real ISO 3166-2 subdivision code of
    that country, e.g iso3166-2-flags/GB/GB-ENG.svg.

    Parameters
    ==========
    :iso3166_2_dir: str (default="iso3166-2-flags")
        path to the ISO 3166-2 flag folder.
    :subdivisions: Subdivisions (default=None)
        iso3166-2 Subdivisions object, created if not passed in.

    Returns
    =======
    :errors: list
        list of human-readable problems found, empty if all filenames are valid.
    """
    all_subdivision_codes = (subdivisions or Subdivisions()).subdivision_codes()
    errors = []
    for entry in sorted(os.listdir(iso3166_2_dir)):
        entry_path = os.path.join(iso3166_2_dir, entry)
        if not os.path.isdir(entry_path):
            if entry not in IGNORED_FILES:
                errors.append(f"{entry_path}: file outside of a country sub-folder")
            continue
        if entry not in all_subdivision_codes:
            errors.append(f"{entry_path}: sub-folder is not an ISO 3166-1 alpha-2 code with subdivisions")
            continue
        country_codes = set(all_subdivision_codes[entry])
        for filename in sorted(os.listdir(entry_path)):
            if filename in IGNORED_FILES:
                continue
            name, ext = os.path.splitext(filename)
            file_path = os.path.join(entry_path, filename)
            if ext not in FLAG_EXTENSIONS:
                errors.append(f"{file_path}: unsupported extension {ext or '(none)'}, expected one of {', '.join(FLAG_EXTENSIONS)}")
            if name not in country_codes:
                errors.append(f"{file_path}: {name} is not an ISO 3166-2 subdivision code of {entry}")
    return errors

def validate_flags(flag_dirs: tuple=("iso3166-1-flags", "iso3166-2-flags", "iso3166-3-flags"), iso3166_2_dir: str="iso3166-2-flags") -> list:
    """
    Run the SVG safety check over every SVG in flag_dirs and the filename check over iso3166_2_dir,
    returning all problems found.
    """
    errors = []
    for flag_dir in flag_dirs:
        for folder_path, _, filenames in os.walk(flag_dir):
            for filename in sorted(filenames):
                if filename.lower().endswith(".svg"):
                    errors += check_svg_safety(os.path.join(folder_path, filename))
    if iso3166_2_dir:
        errors += check_iso3166_2_filenames(iso3166_2_dir)
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check the flag SVGs are safe to inline and the ISO 3166-2 flag filenames are valid subdivision codes.')
    parser.add_argument('-flag_dirs', '--flag_dirs', type=str, required=False, default="iso3166-1-flags,iso3166-2-flags,iso3166-3-flags",
        help='Comma-separated list of flag folders whose SVGs are safety checked.')
    parser.add_argument('-iso3166_2_dir', '--iso3166_2_dir', type=str, required=False, default="iso3166-2-flags",
        help='ISO 3166-2 flag folder whose filenames are validated, pass an empty string to skip.')
    args = parser.parse_args()

    errors = validate_flags(tuple(d.strip() for d in args.flag_dirs.split(",") if d.strip()), args.iso3166_2_dir)
    for error in errors:
        print(error)
    print(f"{len(errors)} problem(s) found." if errors else "All flags passed the SVG safety and filename checks.")
    sys.exit(1 if errors else 0)
