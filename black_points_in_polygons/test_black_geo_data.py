
from badook_tests.context import BadookContext
from badook_tests.dsl.summary import NumericSummary, PointSummary, PolygonSummary
from badook_tests.context import BadookContext, Client
from badook_tests.dsl.enums import ComparisonPoint
from badook_tests import DataTestCase
import numpy as np
from scipy import stats
from math import sqrt
from shapely.geometry import Polygon, Point

class BlackTests(DataTestCase):
 
    @classmethod
    def set_up(cls):
        cls.context.set_project_name("Geo_test")
        
        #defining a dataset level summary
        cls.raw_data = cls.context \
                .create_summary(name='raw_data', dataset='raw-track-points')
        
                    
        cls.polygon_data = cls.context \
                .create_summary(name='camera_boundaries_summary',\
                            dataset='camera_boundaries')
             
        
        polygons = PolygonSummary(name='polygon', \
                                feature='boundaries') \
                                .group_by('cameraSource') \
                                .on(cls.polygon_data)
        
        cls.polygon_data.add_summary(polygons)
    
        event_location = PointSummary(name='event_location', \
		 	  			feature=['positionX','positionY']) \
            			.group_by('cameraSource') \
                                .on(cls.raw_data)

        cls.raw_data.add_summary(event_location)
	          
        
    
    def test_event_inside_camera_polygon(self):
        locations =  self.raw_data.get_summary('event_location')
        print('locations: ', locations)
        polygon = self.polygon_data.get_summary('polygon')
        print('polygon: ', polygon)
        def _check_inside (group, poly):
            count = 0
            for point in group:
                if not None in point:
                    if not Point(point).within(Polygon(poly)):
                        count=count+1
            if count>0:
                return False
            return True

        locations.group.compare_to(polygon, calculation ='union') \
            .join_on(on=['cameraSource']) \
            .check(_check_inside).assert_all()


    def test_event_inside_camera_polygon25(self):
        locations =  self.raw_data.get_summary('event_location')
        polygon = self.polygon_data.get_summary('polygon')
        def _check_inside25(group, poly):
            count = 0
            for point in group:
                if not None in point:
                    if not Point(point).within(Polygon(poly)):
                        count=count+1
            if count/len(group)>0.2:
                return False
            return True

        locations.group.compare_to(polygon, calculation ='union') \
            .join_on(on=['cameraSource']) \
            .check(_check_inside25).assert_all()
    
    def test_event_inside_camera_polygon50(self):
        locations =  self.raw_data.get_summary('event_location')
        polygon = self.polygon_data.get_summary('polygon')
        def _check_inside50(group, poly):
            count = 0
            for point in group:
                if not None in point:
                    if not Point(point).within(Polygon(poly)):
                        count=count+1    
            
            if count/len(group)>0.5:
                return False
            return True

        locations.group.compare_to(polygon, calculation ='union') \
            .join_on(on=['cameraSource']) \
            .check(_check_inside50).assert_all()

    def test_event_inside_camera_polygon75(self):
        locations =  self.raw_data.get_summary('event_location')
        polygon = self.polygon_data.get_summary('polygon')
        def _check_inside75(group, poly):
            count = 0
            for point in group:
                if not None in point:
                    if not Point(point).within(Polygon(poly)):
                        count=count+1
            if count/len(group)>0.75:
                return False
            return True

        locations.group.compare_to(polygon, calculation ='union') \
            .join_on(on=['cameraSource']) \
            .check(_check_inside75).assert_all()



