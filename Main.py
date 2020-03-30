"""
Resource for Hub Site Cloning:
Blog: https://www.esri.com/arcgis-blog/products/arcgis-hub/announcements/introducing-arcgis-hub-python-api-for-sites/
GitHub repo for acrgishub module: https://github.com/Esri/hub-py/blob/master/README.md

"""


def main():

    # IMPORTS
    from arcgis.gis import GIS
    import configparser
    import os
    from arcgishub import hub
    import json

    # VARIABLES
    _root_project_path = os.path.dirname(__file__)
    initiative_id = "2df025de8c074d248175994b2e04d4cf"  # Justin's demo

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
    # gis = GIS(url=md_hub_url, username=md_hub_admin, password=md_hub_pwd) # old way??
    # my_hub = gis.hub
    print(f"URL: {md_hub_url}")
    print(f"ADMIN: {md_hub_admin}")
    print(f"PWD: {md_hub_pwd}")
    my_hub = hub.Hub(url=md_hub_url, username=md_hub_admin, password=md_hub_pwd)
    # print(my_hub.enterprise_org_id)
    try:
        print(my_hub.initiatives())
    except json.JSONDecodeError as jde:
        print(f"y_hub.initiatives() returned {jde}")


if __name__ == "__main__":
    main()
