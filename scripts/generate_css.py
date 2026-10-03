import os
import argparse
import re
import copy

#base selectors shared by every generated CSS file. The .fi::before non-breaking space gives the otherwise
#empty <span> a line box - without it the inline-block collapses to 0px high and no flag is visible
BASE_CSS = (
    ".fib {\n"
    "\tbackground-size: contain;\n"
    "\tbackground-position: 50%;\n"
    "\tbackground-repeat: no-repeat;\n"
    "}\n\n"
    ".fi {\n"
    "\tbackground-size: contain;\n"
    "\tbackground-position: 50%;\n"
    "\tbackground-repeat: no-repeat;\n"
    "\tposition: relative;\n"
    "\tdisplay: inline-block;\n"
    "\twidth: 1.33333333em;\n"
    "\tline-height: 1em;\n"
    "}\n\n"
    ".fi::before {\n"
    "\tcontent: \"\\00a0\";\n"
    "}\n\n"
    ".fi.fis {\n"
    "\twidth: 1em;\n"
    "}\n"
)

def css_rule(selector_code: str, flag_path: str, css_dir: str) -> str:
    """
    Return the CSS rule for one flag. CSS url() paths resolve relative to the stylesheet, not the page,
    so the flag path is made relative to the directory the CSS file is served from (e.g. css/iso3166-1.css
    -> ../iso3166-1-flags/ad.svg).
    """
    url = os.path.relpath(flag_path, css_dir or ".").replace(os.sep, "/")
    return f'\n.fi-{selector_code.lower()} {{\n\tbackground-image: url("{url}");\n}}\n'

def create_iso3166_1_css(country_input_folder: str="iso3166-1-flags", export_css_filepath: str="iso3166-1-flags.css", minify: bool=False, css_dir: str=None) -> None:
    """
    Create custom CSS file for all ISO 3166-1 flags. Each flag will have its own custom CSS 
    selector that is linked to the filepath of the flag within the repo, for example: ".fi-al", ".fi-vn"
    and ".fi-za" are the class selectors for Albania, Vietnam & South Africa, respectively. Within 
    each of these selectors, the background-image attribute will be used with a relative link to the
    flag on the repo.

    Parameters
    ==========
    :country_input_folder: string (default="iso3166-1-flags")
        folder where ISO 3166-1 flags are stored on repo.
    :export_css_filepath: str (default="iso3166-1-flags.css")
        export filename for generated ISO 3166-1 CSS file.
    :minify: bool (default=False)
        if True, also writes a minified version to <export_css_filepath>.min.css.
    :css_dir: str (default=None)
        directory the CSS file is served from, which the flag url() paths are made relative to.
        Defaults to the directory of export_css_filepath.

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Input folder of ISO 3166-1 country flags not found.
    """
    #initial css attributes and selector data
    css_output_str = BASE_CSS

    #get list of all ISO 3166-1 flag files, sorted for deterministic output
    all_files = sorted([f for f in os.listdir(country_input_folder) if os.path.isfile(os.path.join(country_input_folder, f))])

    #iterate through all flag files, creating a custom and unique CSS class selector for each
    for code in all_files:
        #ignore readme and ds_store file
        if (os.path.splitext(code)[0].lower() == "readme" or code.lower() == ".ds_store"):
            continue
        css_output_str += css_rule(os.path.splitext(code)[0], os.path.join(country_input_folder, code), css_dir if css_dir is not None else os.path.dirname(export_css_filepath))

    #write full CSS to file in one pass
    with open(export_css_filepath, "w") as css_file:
        css_file.write(css_output_str)

    if minify:
        minified = re.sub(r'\s+', ' ', css_output_str).strip()
        minified = re.sub(r'\s*\{\s*', '{', minified)
        minified = re.sub(r'\s*\}\s*', '}', minified)
        min_filepath = os.path.splitext(export_css_filepath)[0] + ".min.css"
        with open(min_filepath, "w") as min_file:
            min_file.write(minified)

def create_iso3166_2_css(country_input_folder: str="iso3166-2-flags", export_css_filepath: str="iso3166-2-flags.css", minify: bool=False, css_dir: str=None) -> None:
    """
    Create custom CSS file for all ISO 3166-2 flags. Each subdivision flag will have its own custom
    CSS selector that is linked to the filepath of the flag, for example: ".fi-us-tx", ".fi-ga-1"
    and ".fi-lu-ca" are the CSS class selectors for the US State of Texas (US-TX), the Gabonese
    province of Estuaire (GA-1) and the Luxembourgish canton of Capellen (LU-CA), respectively.
    Within each of these selectors, the background-image attribute will be used with a relative
    link to the flag on the repo.

    Parameters
    ==========
    :country_input_folder: string (default="iso3166-2-flags")
        filename of folder for where ISO 3166-2 flags are stored.
    :export_css_filepath: str (default="iso3166-2-flags.css")
        export folder for generated ISO 3166-2 CSS file.
    :minify: bool (default=False)
        if True, also writes a minified version to <export_css_filepath>.min.css.
    :css_dir: str (default=None)
        directory the CSS file is served from, which the flag url() paths are made relative to.
        Defaults to the directory of export_css_filepath.

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Input folder of ISO 3166-2 subdivision flags not found.
    """
    #raise error if folder of ISO 3166-2 flags not present (check before any file operations)
    if not (os.path.isdir(country_input_folder)):
        raise OSError(f"Folder of ISO 3166-2 country flags not found: {country_input_folder}.")

    #initial css attributes and selector data
    css_output_str = BASE_CSS

    #get list of all country sub-folders in ISO 3166-2 folder
    all_folders = sorted([f for f in os.listdir(country_input_folder) if os.path.isdir(os.path.join(country_input_folder, f))])

    #iterate over each subfolder and each subdivision flag, creating a custom and unique CSS class selector for each
    for country in all_folders:
        all_files = [f for f in os.listdir(os.path.join(country_input_folder, country)) if os.path.isfile(os.path.join(country_input_folder, country, f))]
        all_files.sort()
        for file in all_files:
            #ignore readme and ds_store file
            if (os.path.splitext(file)[0].lower() == "readme" or file.lower() == ".ds_store"):
                continue
            css_output_str += css_rule(os.path.splitext(file)[0], os.path.join(country_input_folder, country, file), css_dir if css_dir is not None else os.path.dirname(export_css_filepath))

    #write full CSS to file in one pass
    with open(export_css_filepath, "w") as css_file:
        css_file.write(css_output_str)

    if minify:
        minified = re.sub(r'\s+', ' ', css_output_str).strip()
        minified = re.sub(r'\s*\{\s*', '{', minified)
        minified = re.sub(r'\s*\}\s*', '}', minified)
        min_filepath = os.path.splitext(export_css_filepath)[0] + ".min.css"
        with open(min_filepath, "w") as min_file:
            min_file.write(minified)

#SVG/XLink namespaces shared by the sprite-generation functions below
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

def _new_sprite_root(etree_module):
    """ Create the root <svg> element that <symbol> flags get appended to. """
    #SVG must be the default namespace - a prefixed "ns0:svg" root isn't recognised as SVG when inlined in HTML
    sprite_root = etree_module.Element(f"{{{SVG_NS}}}svg", nsmap={None: SVG_NS, "xlink": XLINK_NS})
    #hidden without display:none, which stops gradients/clip-paths inside the symbols rendering in some browsers
    sprite_root.set("style", "position:absolute;width:0;height:0;overflow:hidden")
    sprite_root.set("aria-hidden", "true")
    sprite_root.set("focusable", "false")
    return sprite_root

def _namespace_ids(symbol, prefix: str) -> None:
    """
    Prefix every id inside a sprite <symbol>, and the url(#id)/href="#id" references to them, so internal
    ids (clip paths, gradients etc.) from different flags don't collide once they share one document.
    """
    elements = [el for el in symbol.iter() if isinstance(el.tag, str) and el is not symbol]
    ids = {el.get("id") for el in elements if el.get("id")}
    if not ids:
        return
    url_ref = re.compile(r"url\(\s*(['\"]?)#([^'\")\s]+)\1\s*\)")
    renamed = lambda m: f"url({m.group(1)}#{prefix}{m.group(2)}{m.group(1)})" if m.group(2) in ids else m.group(0)
    for el in elements:
        for attr, value in el.attrib.items():
            if attr == "id":
                el.set(attr, prefix + value)
            elif attr in ("href", f"{{{XLINK_NS}}}href") and value.startswith("#") and value[1:] in ids:
                el.set(attr, "#" + prefix + value[1:])
            elif "url(" in value:
                el.set(attr, url_ref.sub(renamed, value))
        #url(#id) references inside <style> blocks
        if el.text and "url(" in el.text:
            el.text = url_ref.sub(renamed, el.text)

def _append_svg_symbols(sprite_root, folder: str, id_prefix: str, etree_module) -> int:
    """
    Parse every SVG file directly within folder (non-recursive) and append each as a
    <symbol id="{id_prefix}{code}"> to sprite_root.

    Returns
    =======
    :skipped: int
        number of SVG files skipped due to parse errors.
    """
    skipped = 0
    svg_files = sorted([
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(".svg")
    ])
    for svg_file in svg_files:
        code = os.path.splitext(svg_file)[0].lower()
        svg_path = os.path.join(folder, svg_file)
        try:
            #no external entities/network access - flags come from upstream syncs and contributors
            tree = etree_module.parse(svg_path, etree_module.XMLParser(resolve_entities="internal", no_network=True))  # nosec B320
            src_root = tree.getroot()

            symbol = etree_module.SubElement(sprite_root, f"{{{SVG_NS}}}symbol")
            symbol.set("id", f"{id_prefix}{code}")

            viewbox = src_root.get("viewBox")
            if viewbox:
                symbol.set("viewBox", viewbox)
            else:
                w = src_root.get("width", "")
                h = src_root.get("height", "")
                if w and h:
                    symbol.set("viewBox", f"0 0 {w} {h}")

            for child in src_root:
                symbol.append(copy.deepcopy(child))
            _namespace_ids(symbol, f"{id_prefix}{code}-")
        except Exception:
            skipped += 1
    return skipped

def create_svg_sprite(country_input_folder: str="iso3166-1-flags", export_sprite_filepath: str="css/iso3166-1-sprite.svg") -> None:
    """
    Create an SVG sprite file for all ISO 3166-1 flags using <symbol> elements.
    Each flag is embedded as a <symbol> with id="fi-{alpha2-code}" (e.g. "fi-gb").

    Consume by including the sprite file once in your HTML, then reference flags with:
        <svg><use href="#fi-gb"/></svg>

    Parameters
    ==========
    :country_input_folder: str (default="iso3166-1-flags")
        Folder containing ISO 3166-1 SVG flag files.
    :export_sprite_filepath: str (default="css/iso3166-1-sprite.svg")
        Output path for the generated SVG sprite file.

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Input folder of ISO 3166-1 country flags not found.
    ImportError:
        lxml is required for SVG sprite generation.
    """
    if not os.path.isdir(country_input_folder):
        raise OSError(f"Folder of ISO 3166-1 country flags not found: {country_input_folder}.")

    try:
        from lxml import etree as _etree
    except ImportError:
        raise ImportError("lxml is required for SVG sprite generation. Install with: pip install lxml")

    sprite_root = _new_sprite_root(_etree)
    skipped = _append_svg_symbols(sprite_root, country_input_folder, id_prefix="fi-", etree_module=_etree)

    output_dir = os.path.dirname(export_sprite_filepath)
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    tree_out = _etree.ElementTree(sprite_root)
    tree_out.write(export_sprite_filepath, xml_declaration=True, encoding="utf-8", pretty_print=True)

    if skipped:
        print(f"Warning: {skipped} SVG file(s) were skipped due to parse errors.")

def create_iso3166_2_svg_sprite(country_input_folder: str="iso3166-2-flags", export_sprite_filepath: str="css/iso3166-2-sprite.svg",
                                 per_country: bool=False, export_sprite_dir: str="css/iso3166-2-sprites") -> None:
    """
    Create SVG sprite file(s) for the ISO 3166-2 subdivision flags using <symbol> elements.
    Each flag is embedded as a <symbol> with id="fi-{alpha2-code}-{subdivision-code}"
    (e.g. "fi-us-tx" for the US state of Texas).

    The full ISO 3166-2 dataset spans 2,800+ flags across ~185 country sub-folders, so a single
    combined sprite is impractically large to ship to a browser in one go. By default this function
    still builds one global sprite file (export_sprite_filepath) for convenience/small deployments,
    but set per_country=True to instead generate one much smaller sprite file per country
    (export_sprite_dir/{alpha2-code}.svg) so a UI can lazy-load only the subdivisions it needs.

    Consume by including the required sprite file(s) in your HTML, then reference flags with:
        <svg><use href="#fi-us-tx"/></svg>

    Parameters
    ==========
    :country_input_folder: str (default="iso3166-2-flags")
        Folder containing ISO 3166-2 SVG flag files, nested by country sub-folder.
    :export_sprite_filepath: str (default="css/iso3166-2-sprite.svg")
        Output path for the generated global SVG sprite file (used when per_country=False).
    :per_country: bool (default=False)
        If True, generate one sprite file per country sub-folder instead of a single global sprite.
    :export_sprite_dir: str (default="css/iso3166-2-sprites")
        Output directory for the generated per-country SVG sprite files (used when per_country=True).

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Input folder of ISO 3166-2 subdivision flags not found.
    ImportError:
        lxml is required for SVG sprite generation.
    """
    if not os.path.isdir(country_input_folder):
        raise OSError(f"Folder of ISO 3166-2 country flags not found: {country_input_folder}.")

    try:
        from lxml import etree as _etree
    except ImportError:
        raise ImportError("lxml is required for SVG sprite generation. Install with: pip install lxml")

    all_countries = sorted([
        c for c in os.listdir(country_input_folder) if os.path.isdir(os.path.join(country_input_folder, c))
    ])

    skipped_total = 0

    if per_country:
        if not os.path.isdir(export_sprite_dir):
            os.makedirs(export_sprite_dir, exist_ok=True)

        for country in all_countries:
            sprite_root = _new_sprite_root(_etree)
            skipped_total += _append_svg_symbols(
                sprite_root, os.path.join(country_input_folder, country), id_prefix=f"fi-{country.lower()}-", etree_module=_etree)

            #skip writing an empty sprite file if the country sub-folder has no valid SVG flags
            if len(sprite_root) == 0:
                continue

            export_path = os.path.join(export_sprite_dir, f"{country.lower()}.svg")
            _etree.ElementTree(sprite_root).write(export_path, xml_declaration=True, encoding="utf-8", pretty_print=True)
    else:
        sprite_root = _new_sprite_root(_etree)
        for country in all_countries:
            skipped_total += _append_svg_symbols(
                sprite_root, os.path.join(country_input_folder, country), id_prefix=f"fi-{country.lower()}-", etree_module=_etree)

        output_dir = os.path.dirname(export_sprite_filepath)
        if output_dir and not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        _etree.ElementTree(sprite_root).write(export_sprite_filepath, xml_declaration=True, encoding="utf-8", pretty_print=True)

    if skipped_total:
        print(f"Warning: {skipped_total} SVG file(s) were skipped due to parse errors.")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script for generating the iso3166-1.css, iso3166-2.css and iso3166-3.css files.')

    parser.add_argument('-iso3166_1_country_input_folder', '--iso3166_1_country_input_folder', type=str, required=False, default="iso3166-1-flags",
        help='Input folder of ISO 3166-1 flags.')
    parser.add_argument('-iso3166_2_country_input_folder', '--iso3166_2_country_input_folder', type=str, required=False, default="iso3166-2-flags",
        help='Input folder of ISO 3166-2 flags.')
    parser.add_argument('-iso3166_3_country_input_folder', '--iso3166_3_country_input_folder', type=str, required=False, default="iso3166-3-flags",
        help='Input folder of ISO 3166-3 (former country) flags.')
    parser.add_argument('-export_iso3166_1_css_filepath', '--export_iso3166_1_css_filepath', type=str, required=False, default="iso3166-1-flags-test.css",
        help='Export filepath for generated ISO 3166-1 CSS file.')
    parser.add_argument('-export_iso3166_2_css_filepath', '--export_iso3166_2_css_filepath', type=str, required=False, default="iso3166-2-flags-test.css",
        help='Export filepath for generated ISO 3166-2 CSS file.')
    parser.add_argument('-export_iso3166_3_css_filepath', '--export_iso3166_3_css_filepath', type=str, required=False, default="iso3166-3-flags-test.css",
        help='Export filepath for generated ISO 3166-3 CSS file.')
    parser.add_argument('-iso3166_type', '--iso3166_type', type=str, required=False, default="",
        help='Create the ISO 3166-1, ISO 3166-2 or ISO 3166-3 CSS file. If empty, all three will be generated.')
    parser.add_argument('-css_dir', '--css_dir', type=str, required=False, default=None,
        help='Directory the CSS files will be served from, which flag url() paths are made relative to. Defaults to the directory of each export filepath.')
    parser.add_argument('-minify', '--minify', action='store_true', default=False,
        help='Additionally generate a minified .min.css version of the output CSS file(s).')
    parser.add_argument('-sprite', '--sprite', action='store_true', default=False,
        help='Generate an SVG sprite file for all ISO 3166-1 flags.')
    parser.add_argument('-export_sprite_filepath', '--export_sprite_filepath', type=str,
        required=False, default='css/iso3166-1-sprite.svg',
        help='Export filepath for the generated ISO 3166-1 SVG sprite file.')
    parser.add_argument('-iso3166_2_sprite', '--iso3166_2_sprite', action='store_true', default=False,
        help='Generate an SVG sprite file for all ISO 3166-2 flags.')
    parser.add_argument('-iso3166_2_sprite_per_country', '--iso3166_2_sprite_per_country', action='store_true', default=False,
        help='Generate one smaller ISO 3166-2 SVG sprite file per country instead of a single global sprite (recommended given the dataset size).')
    parser.add_argument('-export_iso3166_2_sprite_filepath', '--export_iso3166_2_sprite_filepath', type=str,
        required=False, default='css/iso3166-2-sprite.svg',
        help='Export filepath for the generated global ISO 3166-2 SVG sprite file (used unless -iso3166_2_sprite_per_country is set).')
    parser.add_argument('-export_iso3166_2_sprite_dir', '--export_iso3166_2_sprite_dir', type=str,
        required=False, default='css/iso3166-2-sprites',
        help='Export directory for the generated per-country ISO 3166-2 SVG sprite files (used when -iso3166_2_sprite_per_country is set).')

    args = parser.parse_args()
    iso3166_1_country_input_folder = args.iso3166_1_country_input_folder
    iso3166_2_country_input_folder = args.iso3166_2_country_input_folder
    export_iso3166_1_css_filepath = args.export_iso3166_1_css_filepath
    export_iso3166_2_css_filepath = args.export_iso3166_2_css_filepath
    iso3166_type = args.iso3166_type
    minify = args.minify

    css_dir = args.css_dir

    if (iso3166_type.lower() in ("", "iso3166-1")):
        create_iso3166_1_css(country_input_folder=iso3166_1_country_input_folder, export_css_filepath=export_iso3166_1_css_filepath, minify=minify, css_dir=css_dir)
    if (iso3166_type.lower() in ("", "iso3166-2")):
        create_iso3166_2_css(country_input_folder=iso3166_2_country_input_folder, export_css_filepath=export_iso3166_2_css_filepath, minify=minify, css_dir=css_dir)
    #ISO 3166-3 is a flat folder like ISO 3166-1, so the same generator applies
    if (iso3166_type.lower() in ("", "iso3166-3")):
        create_iso3166_1_css(country_input_folder=args.iso3166_3_country_input_folder, export_css_filepath=args.export_iso3166_3_css_filepath, minify=minify, css_dir=css_dir)

    if args.sprite:
        create_svg_sprite(country_input_folder=iso3166_1_country_input_folder,
                          export_sprite_filepath=args.export_sprite_filepath)

    if args.iso3166_2_sprite:
        create_iso3166_2_svg_sprite(country_input_folder=iso3166_2_country_input_folder,
                          export_sprite_filepath=args.export_iso3166_2_sprite_filepath,
                          per_country=args.iso3166_2_sprite_per_country,
                          export_sprite_dir=args.export_iso3166_2_sprite_dir)