
#!/usr/bin/env python

from pathlib import Path
from typing import List
import markdown, json
from mrkdwn_analysis import MarkdownAnalyzer as MD
import mkdocs_gen_files
import logging
import shutil 
from typing import Any

logger = logging.getLogger("gen_doc_stubs")


def log(log_string : Any = "log", levels = 0, pref = " -", log_type = "LOG"):
    if levels >= 0:
        log_string = pref*(levels+1) + f">{log_string}"
    print(f"{log_type} {log_string}")

def debug(log_string, levels = 0, pref = " :"):
    pass
    #log(log_string, levels, pref, "DBG")

def info(log_string, levels = 0, pref = " #"):
    log(log_string, levels, pref, "INF")

def warning(log_string, levels = 0, pref = "??"):
    log(log_string, levels, pref, "WRN")

def error(log_string, levels = 0, pref = "!!"):
    log(log_string, levels, pref, "ERR")


def get_title(path: Path, lvl = 0) -> str:
    debug(f"Calling get_title(path={path})", lvl)
    # If there's no title in the MD file, it's not a proper page.
    data = Path(path).read_text(encoding='utf-8')
    md = markdown.Markdown(extensions=['meta'])
    md.convert(data)
    metadata = md.Meta  # type: ignore

    get_summ_links(path)

    if "title" not in metadata:
        log("No Title in .md", lvl)
        return ""
    title = metadata["title"][0]

    # If the title contains <>, then it's a Template page, not meant for Docs
    if "<" in title and ">" in title:
        log(f"Title `{title}` is template.", lvl)
        return ""
    
    # If not invalidated, return the title
    log(f"Title `{title}` found.", lvl)
    return title

def get_summ_links(path: Path, lvl = 0) -> str:
    analyzer = MD(path)
    headers = analyzer.identify_headers()
    debug_path = Path(f"debug/{path}")
    debug_path.parent.mkdir(parents=True, exist_ok=True)
    debug_path.write_text(json.dumps(headers, indent=4))
    return json.dumps(headers, indent=4)


def create_path_to_nav_lookup(start_path : Path, lvl = 0) -> dict:
    debug(f"Calling create_path_to_nav_lookup(start_path={start_path})", lvl)
    url_to_nav = {}
    indices = sorted( list(start_path.glob("**/index.md")) + list(start_path.glob("**/README.md")))
    indices.sort(key=lambda p: len(p.parts))
    for index_path in indices:
        relative_path = index_path.relative_to("docs")
        parts = relative_path.parts
        # TODO add an "If In Nav Exclusions" so people can't poke around at the 404s
        title = get_title(index_path, lvl+2)
        # If there's only one Part in the Path, then this is at the Root level, and at the Root there isn't a difference between Index & Article
        if len(parts) <= 1:
            log(f"Found Root markdown file <{title}>. \n\t PATH: {relative_path}", len(parts) + lvl)
        # If it's an index, add its path to the url_to_nav dict
        else:
            url_to_nav["/".join(parts[:-1])] = title
            log(f"Added part <{parts[-2]}> to nav as <{title}>. \n\t PATH: {relative_path}", len(parts) + lvl)
    return url_to_nav


# Creates a key/value pair for Navigation. Part I might understand least
def get_nav_key(path : Path, title: str, url_to_nav: dict, lvl = 0) -> tuple[tuple[str, ...],str, int]:
    debug(f"Calling get_nav_key(path={path},title={title})", lvl)
    nav_key = ()
    parts = path.parts
    weight = len(parts) if parts[-1] == "index.md" else 5 + len(parts)

    # If there's only one Part in the Path, then this is at the Root level, and at the Root there isn't a difference between Index & Article
    if len(parts) <= 1:
        log(f"Found Root markdown file <{title}>. \n\t PATH: {path}", len(parts) + lvl)
        return (title,) , f"{path}", 0

    # should be guaranteed not to hit the Attribute Error
    for i in range(len(parts)):
        part = parts[i] 
        if ".md" in part:
            if "index" not in part:
                nav_key+=(title,)

        else:
            try:
                nav_key+=(url_to_nav["/".join(parts[:i+1])],)
            except:
                error(url_to_nav)
                raise AttributeError(f"Failed to Convert to NavKey: \n\t Part <{part}> \n\t Path <{path}>")

    nav_val = f"{path}"
    log("::: " + "/".join(nav_key) + " => " + nav_val, lvl)
    return nav_key, nav_val, weight

def add_snippets_to_index():
    pass

def build_from_walk():
    log("build_from_walk START")
    paths = []
    for path in Path("docs").walk():
        print(path)
        paths.append(path)
    log(paths) 
    log("build_from_walk END")

def main():
    build_from_walk()
    log(f"Running gen_doc_stubs.py")
    doc_paths = list(sorted(Path("docs/").glob("**/*.md")))
    error(f"<{doc_paths}>")
    log(f"Found <{len(doc_paths)}> markdown docs")
    nav_items = []
    url_to_nav = create_path_to_nav_lookup(Path("docs/"), 1)
    for path in doc_paths:
        log(f"interpreting `{path}`")
        module_path = path.relative_to("docs").with_suffix(".md")
        log(f"module `{module_path}`", 1)

        title = get_title(path)
        if title:
            nav_items.append(get_nav_key(module_path, title, url_to_nav, 2))
        else:
            log(f"Doc does not have Title, so it's not a Proper File: <{path}>", 1)
            
    log(f"Found <{len(nav_items)}> articles")


    ## Final Output
    nav = mkdocs_gen_files.Nav() # type: ignore
    nav_items.sort(key=lambda item: item[-1]) # TODO: actually use weights. currently, it's all determined by filename.
    for key, val, _ in nav_items:
        nav[key] = val # type: ignore
    with mkdocs_gen_files.open("SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())

    ## Write test outputs
    with open("debug/nav.json", "w") as f:
        print(json.dumps(nav._data, indent=4), file=f)
    with open("debug/url_to_nav.json", "w") as f:
        print(json.dumps(url_to_nav, indent=4), file=f)

    with open("debug/SUMMARY.md", "w") as test_file:
        test_file.writelines(nav.build_literate_nav())


# THIS DOESN'T WORK
if __name__ == "__main__":
    pass
shutil.rmtree("debug")
main()
