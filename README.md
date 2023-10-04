# mvc4kivy (m4k)

Borrowed from the [kivymd's](https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/) 
MVC tool project creator but with some features added
like lazy loading of kv file and lazy adding of screen to improve application speed at startup.

To install run
```bash
pip install mvc4kivy
```

# To create a project

```bash
### Template command:
m4k-createproject name_pattern path_to_project name_project python_version kivy_version

# Example command:
m4k-createprojectt MVC /home/kengoon/PycharmProjects MyMVCProject python3.10 2.1.0
```

This command will by default create a project with an MVC pattern.
Also, the project will create a virtual environment with Python 3.10, Kivy version 2.1.0 and KivyMD master version.


<img src="https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/mvc-base.png"/>

### Creating a project using a database

```bash
# Template command:
m4k-createproject \
    name_pattern \
    path_to_project \
    name_project \
    python_version \
    kivy_version \
    --name_database
    
# Example command:
m4k-createproject \
    MVC \
    /home/kengo/PycharmProjects \
    MyMVCProject \
    python3.10 \
    2.1.0 \
    --name_database firebase
```
This command will create a project with an MVC template by default. 
The project will also create a virtual environment with Python 3.10, Kivy version 2.1.0, KivyMD master version 
and a wrapper for working with the database restdb.io.

### Create project with responsive view

When creating a project, you can specify which views should use responsive behavior. 
To do this, specify the name of the view/views in the –-use_responsive argument:

```bash
# Template command:
m4k-createproject \
    name_pattern \
    path_to_project \
    name_project \
    python_version \
    kivy_version \
    --name_screen FirstScreen SecondScreen ThirdScreen \
    --use_responsive FirstScreen SecondScreen
```

# To add a view

The script creates a new View package in an existing project with an MVC template created using the create_project utility.
### Use a clean architecture for your applications.
To add a new view to an existing project that was created using the create_project utility, use the following command:

```bash
# Template Command:
m4k-addview \
    name_pattern \
    path_to_project \
    name_view
    
# Example Command
m4k-addview \
    MVC \
    /home/kengo/PycharmProjects \
    NewScreen
```

You can also add new views with responsive behavior to an existing project:
```bash
m4k-addview \
    MVC \
    /home/kengoon/PycharmProjects \
    NewScreen \
    --use_responsive yes
```

# To remove a view

```bash
# Template Command:
m4k-rmview \
    name_pattern \
    path_to_project \
    name_view
    
# Example Command
m4k-rmview \
    MVC \
    /home/kengo/PycharmProjects \
    NewScreen
```