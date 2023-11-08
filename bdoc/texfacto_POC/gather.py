from collections import defaultdict
from shutil      import rmtree
from yaml        import safe_load

from natsort import natsorted


TAG_FILE = "file"
TAG_DIR  = "dir"

TAG_TOC  = "toc"

TAG_ABOUT_FILE = "about.yaml"
TAG_TEMP_DOC   = ".tmpdoc"


def dirs2analyze(
    source,
    alldirs
):
    src_about = source / "about.yaml"

    if not src_about.is_file():
        sorteddirs = None

    else:
        with src_about.open(
            encoding='utf8',
            mode='r',
        ) as f:
            about_cfg = safe_load(f)

        sorteddirs = about_cfg.get(TAG_TOC, None)

    if sorteddirs is None:
        sorteddirs = natsorted(alldirs)

    else:
        for i, p in enumerate(sorteddirs):
            if p[-1] != '/':
                TODO_PB

            p  = p[:-1]
            fp = source / p

            if not fp.is_dir():
                TODO_PB

            sorteddirs[i] = fp

    # print([p.name for p in sorting])

    return sorteddirs


def files2analyze(
    onedir,
    allfiles
):
    files_about = onedir / "about.yaml"

    if not files_about.is_file():
        sortedfiles = None

    else:
        with files_about.open(
            encoding='utf8',
            mode='r',
        ) as f:
            about_cfg = safe_load(f)

        sortedfiles = about_cfg.get(TAG_TOC, None)

    if sortedfiles is None:
        sortedfiles = natsorted(allfiles)

    else:
        for i, p in enumerate(sortedfiles):
            fp = onedir / p

            if not fp.is_file():
                TODO_PB

            sortedfiles[i] = fp

    # print([p.name for p in sorting])

    return sortedfiles


def emptydir(folder):
    if folder.is_dir():
        print(f'+ Cleaning the content of the final product folder src/{folder.name}')

        rmtree(folder)

    else:
        print(f'+ Creation of the final product folder {folder.name}')

    folder.mkdir(parents = True)


def build_project(
    source  ,
    treeview
):
    projectname  = source.parent.name
    projectfolder = source.parent / projectname
    tmpdocfolder  = source.parent / TAG_TEMP_DOC

    sorteddirs = dirs2analyze(
        source  = source,
        alldirs = list(treeview[TAG_DIR].keys())
    )

    extradeco = "-"*(2 + len(projectname))

    print(f"""
--------------{extradeco}
FINAL PRODUCT "{projectname}"
--------------{extradeco}
    """)

    emptydir(projectfolder)
    emptydir(tmpdocfolder)

    src2dest = {
        'sty': projectfolder / f"{projectname}.sty",
        'tex': tmpdocfolder / f"{projectname}-doc.tex",
    }

    filesadded = defaultdict(list)

    for onedir in sorteddirs:
        print(f'+ Working in {onedir}')

        content = treeview[TAG_DIR][onedir]

        sortedfiles = files2analyze(
            onedir   = onedir,
            allfiles = list(content[TAG_FILE])
        )

        for onefile in sortedfiles:
            ext = onefile.suffix[1:]
            destfile = src2dest[ext]

            print(
                f'   * [{ext.upper()}] '
                f'Adding content file from {onefile.name}'
                 '\n'
                f'   *       '
                f'                      to {destfile.name}'
            )

            with onefile.open(
                encoding = "utf-8",
                mode = "r"
            ) as f:
                content = f.read()

            with destfile.open(
                encoding = "utf-8",
                mode = "a"
            ) as f:
                f.write('\n')
                f.write(content)
