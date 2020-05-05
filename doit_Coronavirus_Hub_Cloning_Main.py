"""
Clone a Hub Site and Initiative and all subpages, then rename and move cloned items to the designated backup folder.
Establish a connection to arcgis online hub using arcgishub module from ESRI. Get the initiative item of interest.
Clone the item and move the cloned initiative and application to the backup folder. Create a standard arcgis api
for python gis connection and search for cloned subpage items by name. The subpage names follow a format ending in
what appears to be milliseconds since epoch timestamp. Perform checks on the item title to ensure clone related,
and then rename the item. Then move the subpage items to the backup folder.

NOTE: Requires src folder for arcgishub module, pulled down from ESRI GitHub, in project directory

ISSUE: When moved to server can't pip install arcgis hub, think because can't connect to github from server.
    Command for install is: pip install -e git+https://github.com/esridc/hub-py.git#egg=arcgishub
    To get/install git on the server you also have to connect to github it seems.
    Will attempt to get/access arcgishub module through ArcPro.
ISSUE: When pages are cloned their url is revised to end in "-copy-<milliseconds time stamp>". When this happens
    the page links on the main hub application no longer route. Example, the Business Resources page becomes asset
    Business Resources-copy-1585912032090 with a url of "/pages/business-resources-copy-1585912032090"
    RESOLUTION: Query for clone related subpages using certain keywords. Filter further and check names to be sure
    they contain '-copy-' and end in an int castable value as this appears to be the naming convention ESRI programmed
    into the hub module functionality. For identified items, revise the title of the item and move the item into the
    backup folder.

Resource for Hub Site Cloning:
Blog: https://www.esri.com/arcgis-blog/products/arcgis-hub/announcements/introducing-arcgis-hub-python-api-for-sites/
GitHub repo for acrgishub module: https://github.com/Esri/hub-py/blob/master/README.md

Author: CJuice
Created: April 2020
Revisions:
20200505, CJuice: completed subpage content query, title rename, and move subpage items to backup
    folder functionality.
"""


def main():

    # IMPORTS
    from arcgishub import hub
    from arcgis.gis import GIS

    import configparser
    import datetime
    import os

    # VARIABLES
    date_format = "%Y%m%d %H%M"
    max_items = 5000
    mdimapdatacatalog_str = "mdimapdatacatalog"
    date_now_formatted = datetime.datetime.now().strftime(date_format)
    backup_text = f"{date_now_formatted} Backup"

    # # Production versions
    # clone_to_folder = "Covid Site Backups"  # PROD
    # initiative_id = "5a9bc8dfb3e54817ac61fa4d8aa33cc0"  # PROD

    # Development versions
    clone_to_folder = "Hub Clone Automation DEVELOPMENT"  # DEV
    initiative_id = "5d230c46f10b4c91a60c54e9bca879b6"  # DEV, J's demo site cloned to mdimapdatacatalog account

    # Credentials access and variable creation
    _root_project_folder = os.path.dirname(__file__)
    credentials_file = fr"{_root_project_folder}\Credentials\Credentials.cfg"
    assert os.path.exists(credentials_file)

    config_parser = configparser.ConfigParser()
    config_parser.read(credentials_file)

    md_url = config_parser["DEFAULT"]["url_maps"]
    md_admin = config_parser["DEFAULT"]["login"]
    md_pwd = config_parser["DEFAULT"]["password"]

    # FUNCTIONS
    def check_title_for_seconds_ending(value: str) -> bool:
        """
        Check the parameter for presence of '-copy-', split on dashes (-), cast last value to int, return boolean
        :param value: title string of the item of interst
        :return: boolean indicating if title ends in seconds timestamp or not
        """
        if "-copy-" not in value:
            return False

        title_parts_list = value.split("-")
        ending = title_parts_list[-1]
        try:
            int(ending)
        except TypeError as te:
            return False
        else:
            return True

    def find_cloned_keywords(title: str) -> bool:
        """
        Iterate over the list of clone related keywords and return True if a keyword is present in the item title.
        title: The title (string) of the item of interest.
        return: Boolean, indicates if a keyword was present or not.
        """
        clone_keywords = ["backup", "copy", "copied", "clone", "cloned"]
        title = title.lower()
        for keyword in clone_keywords:
            if keyword in title:
                return True
        return False

    def revise_cloned_item_title(cloned_title: str, date_time_lead: str) -> str:
        """
        Revise the title parameter and return the modified string
        :param cloned_title: string title of the item of interest
        :param date_time_lead: formatted datetime string
        :return: string new title for item
        """
        title_parts = cloned_title.split("-")
        subpage_name, *rest = title_parts
        return f"{date_time_lead} Backup {subpage_name}"

    # FUNCTIONALITY
    # HUB CLONING
    # Need a connection to the hub using the "new" arcgishub module and explore visibility of target initiative.
    #   See note on source of module in top documentation
    # TODO: Monitor for thrown exceptions and then add handling
    my_hub_arcgishub = hub.Hub(url=md_url, username=md_admin, password=md_pwd)

    # Need the initiative of focus (Coronavirus)
    target_initiative_arcgishub = my_hub_arcgishub.initiatives.get(initiative_id)
    print(f"Initiative title: {target_initiative_arcgishub.title}")

    # Need to clone the initiative and the application (site)
    # Takes a few minutes to complete
    new_hub_title = f"{backup_text} {target_initiative_arcgishub.title}"
    print(f"Cloning items to folder '{clone_to_folder}'")
    print(f"Backup Initiative & App titles will be '{new_hub_title}'")
    cloned_initiative_arcgishub = my_hub_arcgishub.initiatives.clone(target_initiative_arcgishub,
                                                                     title=f"{new_hub_title}")
    cloned_appsite_arcgishub = my_hub_arcgishub.sites.get(cloned_initiative_arcgishub.site_id)

    # CONTENT MOVEMENT
    # Move initiative item and application item to backup folder, then go after subpages
    # EXCEPTION thrown when item already exists in folder, either because of duplicated names or item already in folder
    print("Moving cloned initiative and application...")
    move_initiative_result = cloned_initiative_arcgishub.item.move(folder=clone_to_folder)
    move_application_result = cloned_appsite_arcgishub.item.move(folder=clone_to_folder)
    print(f"\tMove Initiative response: {move_initiative_result}")
    print(f"\tMove Application response: {move_application_result}")

    # Need a standard AGOL GIS instance to access AGOL content. Run from an administrator level account.
    gis_conn_standard = GIS(url=md_url, username=md_admin, password=md_pwd)

    # Need the mdimapdatacatalog user object to interrogate for content
    mdimapdatacatalog_user = gis_conn_standard.users.get(mdimapdatacatalog_str)

    # Need an inventory of the items in the root folder
    root_folder_content_list = mdimapdatacatalog_user.items(folder=None, max_items=max_items)

    # Build a dict of item id to item title.
    item_id_title_dict = {item_obj.id: item_obj.title for item_obj in root_folder_content_list}

    # Need to isolate clone related content among items in root folder
    clone_related_content = ({item_id: title for item_id, title in item_id_title_dict.items()
                              if find_cloned_keywords(title)})

    # Need to be extra sure about title so check items from initial inspection per function
    title_checked_clone_related_content = {item_id: title for item_id, title in clone_related_content.items()
                                           if check_title_for_seconds_ending(title)}

    print(f"Items identified as clone related subpages; will be moved to {mdimapdatacatalog_str} > {clone_to_folder}")
    for item_id, item_title in title_checked_clone_related_content.items():
        print(f"\tItem: {item_id} \t {item_title}")

    print("Updating subpage titles and moving to backup folder...")
    for item_id in title_checked_clone_related_content.keys():
        item = gis_conn_standard.content.get(item_id)
        title_update_result = item.update(item_properties={"title": revise_cloned_item_title(cloned_title=item.title,
                                                                                             date_time_lead=date_now_formatted)})
        print(f"\tUpdate title response: {title_update_result}")
        subpage_move_result = item.move(folder=clone_to_folder, owner=mdimapdatacatalog_str)
        print(f"\tMove Subpage response: {subpage_move_result}")

    print("Process Complete")


if __name__ == "__main__":
    main()
