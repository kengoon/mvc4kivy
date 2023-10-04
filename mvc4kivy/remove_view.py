import os
import posixpath
import re

from mvc4kivy import ArgumentParserWithHelp
from mvc4kivy.create_project import check_camel_case_name_project
from shutil import rmtree


screens_data = """%s

screens = {%s
}"""

screens_comment = """# The screen's dictionary contains the objects of the models and controllers
# of the screens of the application.
"""


def main():
    """The function for removing view(s) to the project."""

    parser = create_argument_parser()
    args = parser.parse_args()

    # pattern_name isn't used currently, will be used if new patterns is added in future
    pattern_name = args.pattern  # noqa F841
    path_to_project = args.directory
    name_view = args.name
    if not os.path.exists(path_to_project):
        parser.error(f"Project <{path_to_project}> does not exist...")

    if name_view[-6:] != "Screen":
        parser.error(
            f"The name of the <{name_view}> screen should contain the word "
            f"'Screen' at the end.\n"
            "For example - '--name_screen MyFirstScreen ...'"
        )

    if name_view not in os.listdir(os.path.join(path_to_project, "View")):
        parser.error(
            f"The <{name_view}> view does not exists in the <{path_to_project}> project..."
        )

    module_name = check_camel_case_name_project(name_view)
    if not module_name:
        parser.error(
            "The name of the screen should be written in camel case style. "
            "\nFor example - 'MyFirstScreen' or 'FirstScreen'"
        )
    module_name = "_".join([name.lower() for name in module_name])
    remove_view(name_view, module_name, path_to_project)
    update_screens_data(name_view, module_name, path_to_project)


def remove_view(
        name_screen: str,
        module_name: str,
        path_to_project: str
) -> None:
    path_to_view = os.path.join(path_to_project, "View", name_screen)
    path_to_controller = os.path.join(path_to_view, "Controller", "components")
    path_to_model = os.path.join(path_to_view, "Model", module_name)
    rmtree(path_to_view)
    os.remove(path_to_controller)
    os.remove(path_to_model)


def update_screens_data(
        name_view: str, module_name: str, path_to_project: str
) -> None:
    with open(
            os.path.join(path_to_project, "View", "screens.py")
    ) as screen_module:
        screen_module = screen_module.read()
        imports = re.findall(
            "from Model.*Model|from Controller.*Controller|from View.*View", screen_module
        )
        screens = ""
        path_to_view = os.path.join(path_to_project, "View")

        for name in os.listdir(path_to_view):
            if os.path.isdir(os.path.join(path_to_view, name)):
                res = re.findall(r"[A-Z][^A-Z]*", name)
                # if res and len(res) == 2 and res[-1] == "Screen":
                if res and len(res) > 1 and res[-1] == "Screen":
                    snake_case = "_"
                    screens += (
                            "\n    '%s': {"
                            "\n        'model': %s,"
                            "\n        'controller': %s,"
                            "\n        'view': %s,"
                            "\n        'kv': %s"
                            "\n    },\n"
                            % (
                                f"{' '.join(res).lower()}",
                                f'{name}Model',
                                f'{name}Controller',
                                f'{name}View',
                                f'"{posixpath.join("./View", name, f"{snake_case.join(res).lower()}.kv")}"',
                            )
                    )

        imports.remove(f"from Model.{module_name} import {name_view}Model")
        imports.remove(
            f"from Controller.{module_name} import {name_view}Controller"
        )
        imports.remove(f"from View.{name_view}.{module_name} import {name_view}View")
        imports.insert(0, screens_comment)
        screens = screens_data % ("\n".join(imports), screens)

        with open(
                os.path.join(path_to_project, "View", "screens.py"), "w"
        ) as screen_module:
            screen_module.write(screens)


def create_argument_parser() -> ArgumentParserWithHelp:
    parser = ArgumentParserWithHelp(
        prog="remove_view.py",
        allow_abbrev=False,
    )
    parser.add_argument(
        "pattern",
        help="the name of the pattern with which the view will be removed.",
    )
    parser.add_argument(
        "directory",
        help="the directory of the project to which you want to remove a view.",
    )
    parser.add_argument(
        "name",
        help="the name of the view to add to remove from an existing project.",
    )
    return parser
