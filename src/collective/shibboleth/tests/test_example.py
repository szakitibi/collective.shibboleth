import unittest

from Products.CMFPlone.utils import get_installer

from collective.shibboleth.testing import \
    COLLECTIVE_SHIBBOLETH_INTEGRATION_TESTING


class TestExample(unittest.TestCase):

    layer = COLLECTIVE_SHIBBOLETH_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'collective.shibboleth'
        self.assertTrue(self.installer.is_product_installed(pid),
                        'package appears not to have been installed')
