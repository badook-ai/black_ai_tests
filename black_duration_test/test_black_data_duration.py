        
from badook_tests.context import BadookContext
from badook_tests.dsl.summary import CounterSummary, DurationSummary
from badook_tests.dsl.summary import NumericSummary, PointSummary, PolygonSummary
from badook_tests.context import BadookContext, Client
from badook_tests.dsl.enums import ComparisonPoint
from badook_tests import DataTestCase
import numpy as np
from scipy import stats
from math import sqrt



class BlackTests(DataTestCase):

 
    @classmethod
    def set_up(cls):
        cls.context.set_project_name("raw_store_data")
        
        #defining a dataset level summary
        cls.raw_data = cls.context \
            .create_summary(name='raw_data', dataset='raw-track-points')

        CounterSummary(feature='trackUuid', name='local_association') \
                 .group_by('localTrackUuid') \
                 .on(cls.raw_data)

        CounterSummary(feature='localTrackUuid', name='global_to_local_ratio') \
                 .group_by('trackUuid') \
                 .on(cls.raw_data)

        DurationSummary(feature='timestamp', name='local_track_duration') \
                 .group_by('localTrackUuid') \
                 .on(cls.raw_data)

        DurationSummary(feature='timestamp', name='global_track_duration') \
                 .group_by('trackUuid') \
                 .on(cls.raw_data)

    def test_localtrack_associations_to_single_global(self):
        local_association = self.raw_data.get_summary('local_association')

        local_association.count_distinct \
            .check(lambda x: x == 1) \
            .assert_all()

    def test_local_track_is_under_20_min(self):
        local_track_duration = self.raw_data.get_summary('local_track_duration')

        local_track_duration.duration \
            .check(lambda x: x < 20 * 60) \
            .assert_with_tolerance(0.05)

    def test_global_track_is_under_2_hours(self):
        local_track_duration = self.raw_data.get_summary('local_track_duration')

        local_track_duration.duration \
            .check(lambda x: x < 20 * 60) \
            .assert_with_tolerance(0.05) 