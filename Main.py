"""
Resource for Hub Site Cloning:
https://www.esri.com/arcgis-blog/products/arcgis-hub/announcements/introducing-arcgis-hub-python-api-for-sites/
"""


def main():

    # IMPORTS
    from arcgis.gis import GIS
    import configparser
    import os

    # VARIABLES
    _root_project_path = os.path.dirname(__file__)

    # Credentials access and variable creation
    credentials_file = fr"{_root_project_path}\Credentials\Credentials.cfg"
    assert os.path.exists(credentials_file)
    config_parser = configparser.ConfigParser()
    config_parser.read(credentials_file)
    md_hub_url = config_parser["DEFAULT"]["url"]
    md_hub_admin = config_parser["DEFAULT"]["login"]
    md_hub_pwd = config_parser["DEFAULT"]["password"]

    # ASSERTS
    
    # FUNCTIONS

    # CLASSES

    # FUNCTIONALITY
    # Create a gis connection and get the users in the hub
    gis = GIS(url=md_hub_url, username=md_hub_admin, password=md_hub_pwd)

    return


if __name__ == "__main__":
    main()
