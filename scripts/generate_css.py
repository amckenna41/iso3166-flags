import os
import argparse
import re
import copy

def create_iso3166_1_css(country_input_folder: str="iso3166-1-flags", export_css_filepath: str="iso3166-1-flags.css", minify: bool=False) -> None:
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

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Input folder of ISO 3166-1 country flags not found.
    """
    #initial css attributes and selector data
    css_output_str = (
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
        ".fi.fis {\n"
        "\twidth: 1em;\n"
        "}\n"
    )

    #get list of all ISO 3166-1 flag files, sorted for deterministic output
    all_files = sorted([f for f in os.listdir(country_input_folder) if os.path.isfile(os.path.join(country_input_folder, f))])

    #iterate through all flag files, creating a custom and unique CSS class selector for each
    for code in all_files:
        css_output_str += "\n.fi-" + os.path.splitext(code)[0] + " {\n" + "\tbackground-image: url(" + country_input_folder + "/" + code + ");\n}\n"

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

def create_iso3166_2_css(country_input_folder: str="iso3166-2-flags", export_css_filepath: str="iso3166-2-flags.css", minify: bool=False) -> None:
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
    css_output_str = (
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
        ".fi.fis {\n"
        "\twidth: 1em;\n"
        "}\n"
    )

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
            css_output_str += "\n.fi-" + os.path.splitext(file)[0].lower() + " {\n" + "\tbackground-image: url(" + country_input_folder + "/" + country + "/" + file + ");\n}\n"

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

    SVG_NS = "http://www.w3.org/2000/svg"
    XLINK_NS = "http://www.w3.org/1999/xlink"

    sprite_root = _etree.Element(f"{{{SVG_NS}}}svg", nsmap={"xlink": XLINK_NS})
    sprite_root.set("style", "display:none")
    sprite_root.set("aria-hidden", "true")
    sprite_root.set("focusable", "false")

    all_svg_files = sorted([
        f for f in os.listdir(country_input_folder)
        if os.path.isfile(os.path.join(country_input_folder, f)) and f.lower().endswith(".svg")
    ])

    skipped = 0
    for svg_file in all_svg_files:
        code = os.path.splitext(svg_file)[0].lower()
        svg_path = os.path.join(country_input_folder, svg_file)
        try:
            tree = _etree.parse(svg_path)
            src_root = tree.getroot()

            symbol = _etree.SubElement(sprite_root, f"{{{SVG_NS}}}symbol")
            symbol.set("id", f"fi-{code}")

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
        except Exception:
            skipped += 1
            continue

    output_dir = os.path.dirname(export_sprite_filepath)
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    tree_out = _etree.ElementTree(sprite_root)
    tree_out.write(export_sprite_filepath, xml_declaration=True, encoding="utf-8", pretty_print=True)

    if skipped:
        print(f"Warning: {skipped} SVG file(s) were skipped due to parse errors.")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script for generating the iso3166-1.css and iso3166-2.css files.')

    parser.add_argument('-iso3166_1_country_input_folder', '--iso3166_1_country_input_folder', type=str, required=False, default="iso3166-1-flags",
        help='Input folder of ISO 3166-1 flags.')
    parser.add_argument('-iso3166_2_country_input_folder', '--iso3166_2_country_input_folder', type=str, required=False, default="iso3166-2-flags",
        help='Input folder of ISO 3166-2 flags.')
    parser.add_argument('-export_iso3166_1_css_filepath', '--export_iso3166_1_css_filepath', type=str, required=False, default="iso3166-1-flags-test.css",
        help='Export filepath for generated ISO 3166-1 CSS file.')
    parser.add_argument('-export_iso3166_2_css_filepath', '--export_iso3166_2_css_filepath', type=str, required=False, default="iso3166-2-flags-test.css",
        help='Export filepath for generated ISO 3166-2 CSS file.')
    parser.add_argument('-iso3166_type', '--iso3166_type', type=str, required=False, default="",
        help='Create ISO 3166-1 or ISO 3166-2 CSS file. If empty, both will be generated.')
    parser.add_argument('-minify', '--minify', action='store_true', default=False,
        help='Additionally generate a minified .min.css version of the output CSS file(s).')
    parser.add_argument('-sprite', '--sprite', action='store_true', default=False,
        help='Generate an SVG sprite file for all ISO 3166-1 flags.')
    parser.add_argument('-export_sprite_filepath', '--export_sprite_filepath', type=str,
        required=False, default='css/iso3166-1-sprite.svg',
        help='Export filepath for the generated ISO 3166-1 SVG sprite file.')

    args = parser.parse_args()
    iso3166_1_country_input_folder = args.iso3166_1_country_input_folder
    iso3166_2_country_input_folder = args.iso3166_2_country_input_folder
    export_iso3166_1_css_filepath = args.export_iso3166_1_css_filepath
    export_iso3166_2_css_filepath = args.export_iso3166_2_css_filepath
    iso3166_type = args.iso3166_type
    minify = args.minify

    if (iso3166_type.lower() == "iso3166-1"):
        create_iso3166_1_css(country_input_folder=iso3166_1_country_input_folder, export_css_filepath=export_iso3166_1_css_filepath, minify=minify)
    elif (iso3166_type.lower() == "iso3166-2"):
        create_iso3166_2_css(country_input_folder=iso3166_2_country_input_folder, export_css_filepath=export_iso3166_2_css_filepath, minify=minify)
    else:
        create_iso3166_1_css(country_input_folder=iso3166_1_country_input_folder, export_css_filepath=export_iso3166_1_css_filepath, minify=minify)
        create_iso3166_2_css(country_input_folder=iso3166_2_country_input_folder, export_css_filepath=export_iso3166_2_css_filepath, minify=minify)

    if args.sprite:
        create_svg_sprite(country_input_folder=iso3166_1_country_input_folder,
                          export_sprite_filepath=args.export_sprite_filepath)