"""
Inventory mdimapdatacatalog content that are backup items from coronavirus site cloning

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
    config_parser = configparser.ConfigParser()
    config_parser.read(credentials_file)
    md_hub_url = config_parser["DEFAULT"]["url_maps"]
    md_hub_admin = config_parser["DEFAULT"]["login"]
    md_hub_pwd = config_parser["DEFAULT"]["password"]

    # ASSERTS
    
    # FUNCTIONS

    # CLASSES

    # FUNCTIONALITY
    # Create a gis connection and get the users in the hub
    gis = GIS(url=md_hub_url, username=md_hub_admin, password=md_hub_pwd)
    mdimapdatacatalog_user = gis.users.get("mdimapdatacatalog")
    mdimap_folder_objs_list = mdimapdatacatalog_user.folders
    print("Getting list of items in root folder")
    root_folder_content_list = mdimapdatacatalog_user.items(folder=None, max_items=5000)
    print(len(root_folder_content_list))
    for item_obj in root_folder_content_list:
        print(item_obj.title)

    exit()
    groups_list = mdimapdatacatalog_user.groups


    return


if __name__ == "__main__":
    main()