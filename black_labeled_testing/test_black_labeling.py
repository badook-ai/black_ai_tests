from badook_tests.context import BadookContext
from badook_tests.dsl.summary import NumericSummary, PointSummary, PolygonSummary, CounterSummary
from badook_tests.context import BadookContext, Client
from badook_tests.dsl.enums import ComparisonPoint
from badook_tests import DataTestCase
import numpy as np
from scipy import stats
from math import sqrt


class BlackTests(DataTestCase):
 
    @classmethod
    def set_up(cls):
        cls.context.set_project_name("labling_test")
        
        #defining a dataset level summary
        cls.raw_data = cls.context \
                .create_summary(name='labeled__data', dataset='merge-track-points')
                    
        
        count_local = CounterSummary(featur=['locakTrackUuid'], name='local_track_per_merge')\
            .group_by('mergeUUId').on(cls.raw_data)

        cls.raw_data.add_summary(count_local)

        global_count = CounterSummary(featur=['trackUuid'], name='global_track_per_merge')\
            .group_by('mergeUUId').on(cls.raw_data)

        cls.raw_data.add_summary(global_count)
        
        merge_count = CounterSummary(featur=['mergeUUId'], name='merge_track_per_global')\
            .group_by('trackUuid').on(cls.raw_data)

        cls.raw_data.add_summary(merge_count)
    
        def test_portion_of_unchanged_local_tracks(self):
            merged_data = self.raw_data.get_summary('local_track_per_merge')
            merged_data.count_ditinct \
                    .check(lambda count : count>1).assert_with_tollerance(0.25)


        def test_portion_of_changed_global_tracks(self):
            merged_data = self.raw_data.get_summary('global_track_per_merge')
            merged_data.count_ditinct \
                    .check(lambda count : count!=1).assert_with_tollerance(0.50)


        def test_portion_of_swap_points(self):
            merged_data = self.raw_data.get_summary('merge_track_per_global')
            merged_data.count_ditinct \
                    .check(lambda count : count==1).assert_all()




	          
