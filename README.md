# Coronavirus Hub Site Cloning/Backup Process
Clone a Hub Site and Initiative and all subpages, then rename and move cloned items to the designated backup folder.
Establish a connection to arcgis online hub using arcgishub module from ESRI. Get the initiative item of interest.
Clone the item and move the cloned initiative and application to the backup folder. Create a standard arcgis api
for python gis connection and search for cloned subpage items by name. The subpage names follow a format ending in
what appears to be milliseconds since epoch timestamp. Perform checks on the item title to ensure clone related,
and then rename the item. Then move the subpage items to the backup folder.

#### NOTE: Requires src folder for arcgishub module, pulled down from ESRI GitHub, in project directory 

Resources for Hub Site Cloning:
- Blog: https://www.esri.com/arcgis-blog/products/arcgis-hub/announcements/introducing-arcgis-hub-python-api-for-sites/

- GitHub repo for acrgishub module: https://github.com/Esri/hub-py/blob/master/README.md