import ckan.plugins as plugins
import wcst
from raster_plugin_util import RasterUtil


class RasterImportPlugin(plugins.SingletonPlugin):
    """
    Implementation of the raster import functionality in ckan
    This class implements the notify method that determines if a dataset was modified and takes appropiate action
    by either registering the raster data or removing it through WCST
    """
    plugins.implements(plugins.IDomainObjectModification)

    def notify(self, entity, operation):
        print operation
        if operation == "changed":
            if entity.as_dict()['state'] == "deleted":
                pass
        elif operation == "deleted":
            if entity.as_dict()['package_id'] is not None:
                self.delete_coverage(entity.as_dict()['package_id'])
        elif operation == "new":
            if entity.as_dict()['url'] is not None:
                self.insert_coverage(entity.as_dict()['url'], entity.as_dict()['package_id'])

    @staticmethod
    def insert_coverage(coverage_url, dataset_id):
        """
        Inserts a coverage attached to a dataset into the WCST service

        :param coverage_url: string - url to the coverage to be inserted (can be in any gdal supported format + GML)
        :param dataset_id: string - the id of the dataset to which this coverage is attached to
        """
        coverage_local_path = RasterUtil.get_gml_path_from_dataset(coverage_url, dataset_id)
        request = wcst.WCSTInsertRequest(coverage_local_path)
        executor = wcst.WCSTExecutor(RasterUtil.get_wcst_url())
        executor.execute(request)

    @staticmethod
    def delete_coverage(dataset_id):
        """
        Deletes a coverage attached to a dataset from the WCST service
        :param dataset_id: string - the id of the dataset to which this coverage is attached to
        """
        request = wcst.WCSTDeleteRequest(RasterUtil.dataset_id_to_coverage_id(dataset_id))
        executor = wcst.WCSTExecutor(RasterUtil.get_wcst_url())
        executor.execute(request)






