"""
The script creates a new View package
=====================================

The script creates a new View package in an existing project with an MVC
template created using the create_project utility.

.. rubric:: Use a clean architecture for your applications.

To add a new view to an existing project that was created using the
`create_project` utility, use the following command::

    m4k-addview \\
        name_pattern \\
        path_to_project \\
        name_view

Example command::

    m4k-addview \\
        MVC \\
        /Users/macbookair/Projects \\
        NewScreen

You can also add new views with responsive behavior to an existing project::

    m4k-addview \\
        MVC \\
        /Users/macbookair/Projects \\
        NewScreen \\
        --use_responsive yes

For more information about adaptive design,
`see here <https://kivymd.readthedocs.io/en/latest/components/responsivelayout/>`_.
"""

__all__ = [
    "main",
]

import os
import posixpath
import re

from kivy import Logger

from . import ArgumentParserWithHelp
from .create_project import (
    check_camel_case_name_project,
    create_common_responsive_module,
    create_controller,
    create_model,
    create_view,
)

screens_data = """%s

screens = {%s
}
"""

screns_comment = """# The screen's dictionary contains the objects of the models and controllers
# of the screens of the application.
"""

instantiate_responsive_view = ""


def main():
    """The function of adding a new view to the project."""

    global screens_data
    global instantiate_responsive_view

    parser = create_argument_parser()
    args = parser.parse_args()

    # pattern_name isn't used currently, will be used if new patterns is added in future
    pattern_name = args.pattern  # noqa F841
    path_to_project = args.directory
    name_view = args.name
    use_responsive = args.use_responsive
    instantiate_responsive_view = args.instantiate_responsive_view

    if not os.path.exists(path_to_project):
        parser.error(f"Project <{path_to_project}> does not exist...")

    if name_view[-6:] != "Screen":
        parser.error(
            f"The name of the <{name_view}> screen should contain the word "
            f"'Screen' at the end.\n"
            "For example - '--name_screen MyFirstScreen ...'"
        )

    if name_view in os.listdir(os.path.join(path_to_project, "View")):
        parser.error(
            f"The <{name_view}> view also exists in the <{path_to_project}> project..."
        )

    # Create model.
    name_database = (
        "yes"
        if "database.py" in os.listdir(os.path.join(path_to_project, "Model"))
        else "no"
    )
    module_name = check_camel_case_name_project(name_view)
    if not module_name:
        parser.error(
            "The name of the screen should be written in camel case style. "
            "\nFor example - 'MyFirstScreen'"
        )
    module_name = "_".join([name.lower() for name in module_name])
    create_model(name_view, module_name, name_database, path_to_project)

    # Create controller.
    # FIXME: This is not a very good solution in order to understand whether
    #  a project uses a hot reload or not. Because the string
    #  'from kivymd.tools.hotreload.app import MDApp' in the project can just
    #  be commented out and the project does not actually use hot reload.
    with open(os.path.join(path_to_project, "main.py")) as main_module:
        if "from kivymd.tools.hotreload.app import MDApp" in main_module.read():
            use_hotreload = "yes"
        else:
            use_hotreload = "no"
        create_controller(
            name_view, module_name, use_hotreload, path_to_project
        )
    # Create View.
    if use_responsive == "no":
        create_view(name_view, module_name, [], path_to_project)
    else:
        create_view(name_view, module_name, [name_view], path_to_project)
        create_common_responsive_module([name_view], path_to_project)
    # Create 'View.screens.py module'.
    update_screens_data(name_view, module_name, path_to_project)
    Logger.info(
        f"KivyMD: The {name_view} view has been added to the project..."
    )


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

        imports.append(f"from Model.{module_name} import {name_view}Model")
        imports.append(
            f"from Controller.{module_name} import {name_view}Controller"
        )
        imports.append(f"from View.{name_view}.{module_name} import {name_view}View")
        imports.insert(0, screns_comment)
        screens = screens_data % ("\n".join(imports), screens)

        with open(
                os.path.join(path_to_project, "View", "screens.py"), "w"
        ) as screen_module:
            screen_module.write(screens)


def create_argument_parser() -> ArgumentParserWithHelp:
    parser = ArgumentParserWithHelp(
        prog="create_project.py",
        allow_abbrev=False,
    )
    parser.add_argument(
        "pattern",
        help="the name of the pattern with which the project will be created.",
    )
    parser.add_argument(
        "directory",
        help="the directory of the project to which you want to add a new view.",
    )
    parser.add_argument(
        "name",
        help="the name of the view to add to an existing project.",
    )
    parser.add_argument(
        "--use_responsive",
        default="no",
        help="whether to create a view with responsive behavior.",
    )
    parser.add_argument(
        "--instantiate_responsive_view",
        default="yes",
        help="instantiate responsive"
    )
    return parser


if __name__ == "__main__":
    main()
