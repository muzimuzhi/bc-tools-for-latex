from src2prod import *

from texfacto import *

PROJECT_DIR = Path(__file__).parent
SOURCE_DIR  = PROJECT_DIR / Path('src')
TARGET_DIR  = PROJECT_DIR.parent / PROJECT_DIR.name.lower()


# ----------------- #
# -- DEBUG TOOLS -- #
# ----------------- #

def debug_treeview(treeview):
    _recu_debug_treeview(
        treeview = treeview,
        depth = 0
    )

    exit()

def _recu_debug_treeview(
    treeview,
    depth
):
    tab    = "  " * depth
    depth += 2

    for kind, content in treeview.items():
        if kind == TAG_FILE:
            for onefile in content:
                print(f"{tab}* {onefile.name}")

        else:
            for onedir, subtree in content.items():
                print(f"{tab}+ {onedir.name}")

                _recu_debug_treeview(
                    treeview = subtree,
                    depth    = depth
                )



# ----------------------- #
# -- ALL USEFULL FILES -- #
# ----------------------- #

treeview = build_tree(
    project = PROJECT_DIR,
    source  = Path('src'),
    target  = TARGET_DIR,
    readme  = Path('README.md'),
)


# --------------------------------- #
# -- IGNORE THE UNUSED PDF FILES -- #
# --------------------------------- #

for directdir, content in treeview[TAG_DIR].items():
    subfiles = content[TAG_FILE]

# We need to work on a copy.
    for directsubfile in subfiles[:]:
        if directsubfile.suffix == '.tex':
            pdf_unused = directsubfile.parent / f"{directsubfile.stem}.pdf"

            if pdf_unused in subfiles:
                subfiles.remove(pdf_unused)


# ------------------------------ #
# -- ONLY SOURCE FILES SORTED -- #
# ------------------------------ #

debug_treeview(treeview)


allfiles_sorted = build_tree_sorted(
    source   = SOURCE_DIR,
    allfiles = treeview
)


# -------------------- #
# -- XXXXXX -- #
# -------------------- #

for f in treeview:
    if f.suffix == ".sty":
        print(f.name)
