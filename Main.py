"""
Resource for Hub Site Cloning:
Blog: https://www.esri.com/arcgis-blog/products/arcgis-hub/announcements/introducing-arcgis-hub-python-api-for-sites/
GitHub repo for acrgishub module: https://github.com/Esri/hub-py/blob/master/README.md

"""


def main():

    # IMPORTS
    from arcgishub import hub

    import configparser
    import datetime
    import os

    # VARIABLES
    # # # initiative_id = "5a9bc8dfb3e54817ac61fa4d8aa33cc0"  # PROD
    initiative_id = "5d230c46f10b4c91a60c54e9bca879b6"  # J's demo site cloned to mdimapdatacatalog account

    # TODO: Search for a format that doesn't result in an unusable url
    date_format = "%y%m%d-%H%M"
    # backup_text = f"DEVCovidBackup-{datetime.datetime.now().strftime(date_format)}"  # Valid url format
    backup_text = f"{datetime.datetime.now().strftime(date_format)}-DEVCovidBackup"

    # Credentials access and variable creation
    _root_project_folder = os.path.dirname(__file__)
    credentials_file = fr"{_root_project_folder}\Credentials\Credentials.cfg"
    assert os.path.exists(credentials_file)
    config_parser = configparser.ConfigParser()
    config_parser.read(credentials_file)

    # md_url = config_parser["DEFAULT"]["url_hub"]
    md_url = config_parser["DEFAULT"]["url_maps"]
    md_admin = config_parser["DEFAULT"]["login"]
    md_pwd = config_parser["DEFAULT"]["password"]

    # Destination folder for clones
    clone_to_folder = "Hub Clone Automation DEVELOPMENT"

    # FUNCTIONALITY
    # Create a connection to the hub using the "new" arcgishub module and explore visibility of target initiative
    my_hub_arcgishub = hub.Hub(url=md_url, username=md_admin, password=md_pwd)

    # Gets a specific initiative
    target_initiative_arcgishub = my_hub_arcgishub.initiatives.get(initiative_id)
    print(f"Initiative title: {target_initiative_arcgishub.title}")

    # This seems to take a few minutes to complete
    # Clone the initiative and the application (site)
    cloned_initiative_arcgishub = my_hub_arcgishub.initiatives.clone(target_initiative_arcgishub,
                                                                     title=f"{backup_text}")
    cloned_application_arcgishub = my_hub_arcgishub.sites.get(cloned_initiative_arcgishub.site_id)

    # Move initiative item and application item to backup folder
    # EXCEPTION thrown when item already exists in folder, either because of duplicated names or item already in folder
    move_initiative_result = cloned_initiative_arcgishub.item.move(folder=clone_to_folder)
    move_application_result = cloned_application_arcgishub.item.move(folder=clone_to_folder)
    print(f"Move Initiative response: {move_initiative_result}")
    print(f"Move Application response: {move_application_result}")


if __name__ == "__main__":
    main()
