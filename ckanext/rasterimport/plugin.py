import ckan.plugins as plugins


class RasterImportPlugin(plugins.SingletonPlugin):
    """
    Implementation of the raster import functionality in ckan
    This class implements the notify method that determines if a dataset was modified and takes appropiate action
    by either registering the raster data or removing it through WCST
    """
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IConfigurable, inherit=True)

    def before_map(self, map):
        """
        Adds the url mappings to the raster import controller
        """
        map.connect("raster-publish", "/api/raster/publish/{resource_id}",
                    controller='ckanext.rasterimport.controllers.import:RasterImportController', action='publish',
                    resource_id='{resource_id}')
        map.connect("raster-delete", "/api/raster/delete/{resource_id}",
                    controller='ckanext.rasterimport.controllers.import:RasterImportController', action='delete',
                    resource_id='{resource_id}')
        return map

    def update_config(self, config):
        """
        Exposes the public folder of this extension. The intermediary gml files will be stored here.
        """
        plugins.toolkit.add_public_directory(config, 'public')
