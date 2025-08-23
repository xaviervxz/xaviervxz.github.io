
#!/usr/bin/env python

from pathlib import Path
from typing import List
import markdown, json
import mkdocs_gen_files

debug = False

def log(log_string, to_print=False):
    if debug or to_print:
        print(log_string)

nav = mkdocs_gen_files.Nav() # type: ignore

def get_title(path: Path) -> str:
    # If there's no title in the MD file, it's not a proper page.
    data = Path(path).read_text(encoding='utf-8')
    md = markdown.Markdown(extensions=['meta'])
    md.convert(data)
    metadata = md.Meta  # type: ignore

    if "title" not in metadata:
        return ""
    title = metadata["title"][0]

    # If the title contains <>, then it's a Template page, not meant for Docs
    if "<" in title and ">" in title:
        return ""
    
    # If not invalidated, return True
    return title

url_to_nav = {}

def create_path_to_nav_lookup(start_path : Path) -> None:
    indices = list(sorted(start_path.glob("**/index.md")))
    indices.sort(key=lambda p: len(p.parts))
    for index_path in indices:
        relative_path = index_path.relative_to("docs")
        parts = relative_path.parts
        title = get_title(index_path)
        # If there's only one Part in the Path, then this is at the Root level, and at the Root there isn't a difference between Index & Article
        if len(parts) <= 1:
            log(f">> Found Root markdown file <{title}>. \n\t PATH: {relative_path}")
        # If it's an index, add its path to the url_to_nav dict
        else:
            url_to_nav["/".join(parts[:-1])] = title
            log(f">> Added part <{parts[-2]}> to nav as <{title}>. \n\t PATH: {relative_path}")


# Creates a key/value pair for Navigation
def get_nav_key(path : Path, title: str) -> tuple[tuple[str, ...],str, int]:
    nav_key = ()
    parts = path.parts
    weight = len(parts) if parts[-1] == "index.md" else 5 + len(parts)

    # If there's only one Part in the Path, then this is at the Root level, and at the Root there isn't a difference between Index & Article
    if len(parts) <= 1:
        log(f">> Found Root markdown file <{title}>. \n\t PATH: {path}")
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
                log(url_to_nav)
                raise AttributeError(f"Failed to Convert to NavKey: \n\t Part <{part}> \n\t Path <{path}>")

    nav_val = f"{path}"
    log("::: " + "/".join(nav_key) + " => " + nav_val)
    return nav_key, nav_val, weight



log(f"Running gen_doc_stubs.py", True)
doc_paths = list(sorted(Path("docs/").glob("**/*.md")))
create_path_to_nav_lookup(Path("docs/"))
log(doc_paths)
nav_items = []
for path in doc_paths:
    log(f"\n    ==> {path}")
    module_path = path.relative_to("docs").with_suffix(".md")

    title = get_title(path)
    if title:
        nav_items.append(get_nav_key(module_path, title))
    else:
        log(f"Doc not a Proper File: <{path}>")
        
nav_items.sort(key=lambda item: item[-1])
for key, val, _ in nav_items:
    nav[key] = val # type: ignore


with mkdocs_gen_files.open("SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())


if debug:
    with open("nav.json", "w") as nav_f:
        print(json.dumps(nav._data, indent=4), file=nav_f)

    with open("test_SUMMARY.md", "w") as test_file:
        test_file.writelines(nav.build_literate_nav())

