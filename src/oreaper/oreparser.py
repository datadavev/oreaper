'''
Implements extension to d1_common.resource_map to assist with
populating an index of ORE relationships.
'''

import logging
from d1_common import resource_map


class OreParser(resource_map.ResourceMap):

  def getRelations(self):
    '''
    Retrieve the dataset relationships from package.

    Returns: {
        metadata_pids: [],
        resource_map_pids: [],
        data_pids: []
      }
    '''
    res = {"metadata_pids":[],
           "resource_map_pids": [],
           "data_pids": []
           }
    res["resource_map_pids"].append(self.getResourceMapPid())
    res["metadata_pids"] = self.getAggregatedScienceMetadataPids()
    res["data_pids"] = self.getAggregatedScienceDataPids()
    return res

