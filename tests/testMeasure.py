import unittest
import time
from TimePoints import Measure as Measure


class MeasureTestCase(unittest.TestCase):

    def test_call(self):
        Measure.clear()
        Measure.sleep
        time.sleep(1)
        Measure.sleep()

    def test_duration1(self):
        Measure.clear()
        sleep = Measure.sleep
        time.sleep(1.5)
        Measure.sleep
        self.assertTrue(
            sleep.duration > 1, 'sleep duration is not greater then 1')

    def test_duration2(self):
        Measure.clear()
        sleep = Measure.sleep
        time.sleep(1)
        Measure.sleep
        time.sleep(1.5)
        Measure.sleep
        self.assertTrue(
            sleep[0].duration > 2, 'sleep duration is not greater then 2')
        time.sleep(1)
        self.assertTrue(
            Measure.sleep[0].duration > 3,
            'sleep duration is not greater then 3')

    def test_summary1(self):
        Measure.clear()
        some_operation_stats = Measure.some_operation
        time.sleep(1)
        Measure.some_operation
        time.sleep(1)
        Measure.some_operation
        some_operation_stats.summary()

    def test_summary2(self):
        Measure.clear()
        Measure.Building
        time.sleep(2)
        Measure.Building(format='{name} last: {humanized_duration}')
        Measure.Deploying
        time.sleep(1)
        Measure.Deploying(format='{name} last: {humanized_duration}')
        Measure.summary()

    def test_changeComparisonPoint(self):
        Measure.clear()
        some_operation_stats = Measure.some_operation
        time.sleep(1)
        Measure.some_operation
        time.sleep(1)
        Measure.some_operation
        time.sleep(1)
        Measure.some_operation
        some_operation_stats[0](
            format='Duration of {name} from point 0: {hduration}')
        some_operation_stats[1](
            format='Duration of {name} from point 1: {hduration}')
        some_operation_stats[2](
            format='Duration of {name} from point 2: {hduration}')

    def test_loop1(self):
        Measure.clear()
        for i in range(5):
            Measure.loop()
            time.sleep(1)

    def test_loop2(self):
        Measure.clear()
        for i in range(5):
            Measure.loop()
            time.sleep(1)
        Measure.loop[0]()

    def test_loop3(self):
        Measure.clear()
        for i in range(5):
            Measure.loop
            time.sleep(1)
        for i in range(5):
            Measure.loop2
            time.sleep(1)
        Measure.summary()

    def test_loop4(self):
        Measure.clear()
        for i in range(5):
            Measure.loop
            time.sleep(1)
        Measure.loop.summary().squeeze().summary()

    def test_customFormat1(self):
        Measure.clear()
        from logging import warning
        Measure.a
        time.sleep(1)
        warning(Measure.a.to_string(
            format='Why "{name}" took so long: {hduration}!'))

    def test_customFormat2(self):
        Measure.clear()
        Measure.building
        time.sleep(1)
        Measure.building(format='How long was the {name} process: {hduration}')

    def test_customFormat3(self):
        Measure.clear()
        Measure.set_format(
            format='How long was the {name} process: {hduration}')
        Measure.building
        time.sleep(1)
        Measure.building()
        Measure.deploying
        time.sleep(1)
        Measure.deploying()

    def test_customFormat4(self):
        Measure.clear()
        Measure.building.set_format(
            format='How long was the {name} process: {hduration}')
        time.sleep(1)
        Measure.building()
        time.sleep(1)
        Measure.building()

    def test_customFormat5(self):
        Measure.clear()
        Measure.set_format(
            format='Stage {stage_number} of {name} process: {hduration}')
        Measure.building
        time.sleep(1)
        Measure.building(stage_number=1)
        time.sleep(1)
        Measure.building(stage_number=2)


if __name__ == '__main__':
    unittest.main()
