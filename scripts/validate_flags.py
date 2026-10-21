import os
import re
import sys
import argparse
from lxml import etree
from PIL import Image
from iso3166_2 import Subdivisions

#no external entities/network access - flags come from upstream syncs and contributors
SAFE_XML_PARSER = etree.XMLParser(resolve_entities="internal", no_network=True)

#script URLs, and references that make the browser fetch a remote resource (http(s):// or protocol-relative //)
SCRIPT_URL = re.compile(r"^\s*(javascript|vbscript):", re.IGNORECASE)
REMOTE_URL = re.compile(r"^\s*(https?:)?//", re.IGNORECASE)
CSS_REMOTE_URL = re.compile(r"url\(\s*['\"]?\s*((https?:)?//|javascript:)|@import", re.IGNORECASE)

FLAG_EXTENSIONS = (".svg", ".png", ".jpg", ".jpeg")
IGNORED_FILES = {"README.md", ".DS_Store"}

#raster formats each extension must actually contain, as detected by Pillow from the file's content
RASTER_FORMATS = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG"}

#url(#id) references to elements within the same SVG
LOCAL_URL_REF = re.compile(r"url\(\s*['\"]?#([^'\")\s]+)")

#flags whose artwork references symbols/gradients/clip paths that were never included in the file, so part of the
#design doesn't draw - these predate the check and need re-sourcing (e.g from Wikimedia Commons), remove each entry
#once its flag has been replaced. Any other flag with a missing reference fails validation
KNOWN_BROKEN_REFERENCES = {
    "iso3166-2-flags/AD/AD-03.svg", "iso3166-2-flags/BH/BH-17.svg", "iso3166-2-flags/CU/CU-06.svg",
    "iso3166-2-flags/EC/EC-H.svg", "iso3166-2-flags/FR/FR-82.svg", "iso3166-2-flags/FR/FR-NC.svg",
    "iso3166-2-flags/GB/GB-BDF.svg", "iso3166-2-flags/GB/GB-CBF.svg", "iso3166-2-flags/GT/GT-01.svg",
    "iso3166-2-flags/HU/HU-KM.svg", "iso3166-2-flags/IT/IT-AG.svg", "iso3166-2-flags/IT/IT-CS.svg",
    "iso3166-2-flags/IT/IT-FG.svg", "iso3166-2-flags/IT/IT-LE.svg", "iso3166-2-flags/IT/IT-RM.svg",
    "iso3166-2-flags/MK/MK-208.svg", "iso3166-2-flags/MM/MM-07.svg", "iso3166-2-flags/MN/MN-065.svg",
    "iso3166-2-flags/MX/MX-GUA.svg", "iso3166-2-flags/MX/MX-OAX.svg", "iso3166-2-flags/MY/MY-16.svg",
    "iso3166-2-flags/PE/PE-LOR.svg", "iso3166-2-flags/RU/RU-SAM.svg",
}

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
            #event handlers are "on" + letters e.g onload - Inkscape attributes such as only_selected aren't
            if re.fullmatch(r"on[a-z]+", name.lower()):
                errors.append(f"{svg_path}: event handler attribute {name} on <{tag}>")
            elif SCRIPT_URL.search(value):
                errors.append(f"{svg_path}: script URL in {name} on <{tag}>")
            elif name == "href" and REMOTE_URL.search(value):
                errors.append(f"{svg_path}: remote href {value.strip()[:60]} on <{tag}>")
            elif name == "style" and CSS_REMOTE_URL.search(value):
                errors.append(f"{svg_path}: remote url in style on <{tag}>")
    return errors

def check_svg_references(svg_path: str) -> list:
    """
    Check every internal reference in an SVG - href="#id" and url(#id) in attributes, plus url(#id) in <style>
    rules whose class is used - points at an element that exists in the file. A missing target means that part
    of the flag isn't drawn (or is drawn without its fill/clip). Inkscape shape-inside text-flow references are
    ignored, as browsers don't support them and lay the text out from its own x/y instead.

    Parameters
    ==========
    :svg_path: str
        path to the SVG file.

    Returns
    =======
    :errors: list
        list of human-readable problems found, empty if every reference resolves.
    """
    try:
        root = etree.parse(svg_path, SAFE_XML_PARSER).getroot()  # nosec B320
    except etree.XMLSyntaxError:
        #reported by check_svg_safety
        return []

    elements = [el for el in root.iter() if isinstance(el.tag, str)]
    ids = {el.get("id") for el in elements if el.get("id")}
    classes = {c for el in elements for c in (el.get("class") or "").split()}

    missing = set()
    for el in elements:
        for attr, value in el.attrib.items():
            if etree.QName(attr).localname == "href" and value.startswith("#") and value[1:] not in ids:
                missing.add(value[1:])
            #strip Inkscape shape-inside declarations before looking for url() references
            value = re.sub(r"shape-inside\s*:\s*url\([^)]*\)", "", value)
            missing.update(m.group(1) for m in LOCAL_URL_REF.finditer(value) if m.group(1) not in ids)
        if etree.QName(el).localname == "style" and el.text:
            for rule in re.finditer(r"([^{}]+)\{([^}]*)\}", el.text):
                if any(selector.strip().lstrip(".") in classes for selector in rule.group(1).split(",")):
                    missing.update(m.group(1) for m in LOCAL_URL_REF.finditer(rule.group(2)) if m.group(1) not in ids)

    return [f"{svg_path}: reference to missing element #{ref}" for ref in sorted(missing)]

def check_file_format(file_path: str) -> list:
    """
    Check a PNG/JPG/JPEG flag's content is actually in the format its extension says, e.g a WEBP saved as .png.

    Parameters
    ==========
    :file_path: str
        path to the raster flag file.

    Returns
    =======
    :errors: list
        list of human-readable problems found, empty if the format matches.
    """
    expected = RASTER_FORMATS.get(os.path.splitext(file_path)[1].lower())
    if expected is None:
        return []
    try:
        with Image.open(file_path) as img:
            actual = img.format
            img.verify()
    except Exception as e:
        return [f"{file_path}: unreadable image ({e})"]
    return [] if actual == expected else [f"{file_path}: content is {actual}, not {expected} as its extension says"]

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
    Run the SVG safety and reference checks over every SVG in flag_dirs, the format check over every PNG/JPG,
    and the filename check over iso3166_2_dir, returning all problems found. Flags in KNOWN_BROKEN_REFERENCES
    are exempt from the reference check, but are reported once they no longer need the exemption.
    """
    errors = []
    for flag_dir in flag_dirs:
        for folder_path, _, filenames in os.walk(flag_dir):
            for filename in sorted(filenames):
                file_path = os.path.join(folder_path, filename)
                if filename.lower().endswith(".svg"):
                    errors += check_svg_safety(file_path)
                    reference_errors = check_svg_references(file_path)
                    known = os.path.normpath(file_path).replace(os.sep, "/") in KNOWN_BROKEN_REFERENCES
                    if known and not reference_errors:
                        errors.append(f"{file_path}: no longer has missing references, remove it from KNOWN_BROKEN_REFERENCES")
                    elif not known:
                        errors += reference_errors
                else:
                    errors += check_file_format(file_path)
    if iso3166_2_dir:
        errors += check_iso3166_2_filenames(iso3166_2_dir)
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check the flag SVGs are safe to inline with no missing internal references, raster flags match their extension, and the ISO 3166-2 flag filenames are valid subdivision codes.')
    parser.add_argument('-flag_dirs', '--flag_dirs', type=str, required=False, default="iso3166-1-flags,iso3166-2-flags,iso3166-3-flags",
        help='Comma-separated list of flag folders whose SVGs are safety checked.')
    parser.add_argument('-iso3166_2_dir', '--iso3166_2_dir', type=str, required=False, default="iso3166-2-flags",
        help='ISO 3166-2 flag folder whose filenames are validated, pass an empty string to skip.')
    args = parser.parse_args()

    errors = validate_flags(tuple(d.strip() for d in args.flag_dirs.split(",") if d.strip()), args.iso3166_2_dir)
    for error in errors:
        print(error)
    print(f"{len(errors)} problem(s) found." if errors else "All flags passed the SVG safety, reference, format and filename checks.")
    sys.exit(1 if errors else 0)
