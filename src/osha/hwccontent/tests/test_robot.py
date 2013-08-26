from  osha.hwccontent.testing import OSHA_HWCCONTENT_FUNCTIONAL_TESTING
from plone.testing import layered
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("tests.robot"),
                layer=OSHA_HWCCONTENT_FUNCTIONAL_TESTING)
    ])
    return suite