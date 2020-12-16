from badook_tests.context import BadookContext
from badook_tests.dsl.summary import NumericSummary, PointSummary, PolygonSummary, CounterSummary
from badook_tests.context import BadookContext, Client
from badook_tests.dsl.enums import ComparisonPoint
from badook_tests import DataTestCase
import numpy as np
from scipy import stats
from math import sqrt
import pandas as pd 

class BlackTests(DataTestCase):
 
    @classmethod
    def set_up(cls):
        cls.context.set_project_name("swap_test")
        
        #defining a dataset level summary
        cls.raw_data = cls.context \
                .create_summary(name='labeled__data', dataset='merge-track-points')
                    
        
        def _swap_point_id(points):
            df = pd.DataFrame(data=list(map(np.ravel, points)), \
                columns= ['mergeUuid', 'timestamp', 'positionX','positionY'])
            df['time'] = pd.to_datetime(df['timestamp'], format = '%Y-%m-%d %H:%M:S.%f')
            df = df.sort_values(by=['time'])
            swap_ind = df.ne(df.shift()).apply(lambda x: x.index.tolist())['mergeUuid'][1::]
            if len(swap_ind>0):
                return df[['positionX', 'positionY']].loc[swap_ind].values.tolist()

        
        swap_points = PointSummary(feature=['mergeUuid', 'timestamp', 'positionX','positionY'], \
            name='swap_points').group_by('trackUuId4').on(cls.raw_data)

        swap_points.add_udc(name = 'swap_point_id', calculation = _swap_point_id)

        
        #swap_points.add_udc(name = 'swap_point_id', calculation = _swap_point_id)       
        
    
    def test_portion_of_unchanged_local_tracks(self):
        pass
        #swp_point = get_summary()
        #swp_point.swap_point_id.compare_to().check(lambda...).assert_a






	          
