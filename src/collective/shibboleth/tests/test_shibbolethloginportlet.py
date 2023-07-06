from plone import api
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from zope.component import getUtility, getMultiAdapter


from collective.shibboleth.portlets import shibbolethloginportlet
# from collective.shibboleth.tests.base_shibbolethloginportlet import TestCase

import unittest

from collective.shibboleth.testing import \
    COLLECTIVE_SHIBBOLETH_INTEGRATION_TESTING, \
    COLLECTIVE_SHIBBOLETH_FUNCTIONAL_TESTING


class TestPortlet(unittest.TestCase):

    layer = COLLECTIVE_SHIBBOLETH_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.folder = api.content.create(
            container=self.portal,
            type="Folder",
            title="test"
        )

    def test_portlet_type_registered(self):
        portlet = getUtility(IPortletType, name='collective.shibboleth.portlets.ShibbolethLoginPortlet')
        self.assertEquals(portlet.addview, 'collective.shibboleth.portlets.ShibbolethLoginPortlet')

    def test_interfaces(self):
        # TODO: Pass any keywoard arguments to the Assignment constructor
        portlet = shibbolethloginportlet.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(IPortletType, name='collective.shibboleth.portlets.ShibbolethLoginPortlet')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        # TODO: Pass a dictionary containing dummy form inputs from the add form
        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], shibbolethloginportlet.Assignment))

    # NOTE: This test can be removed if the portlet has no edit form
    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = shibbolethloginportlet.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.assertTrue(isinstance(editview, shibbolethloginportlet.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)

        # TODO: Pass any keywoard arguments to the Assignment constructor
        assignment = shibbolethloginportlet.Assignment()

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, shibbolethloginportlet.Renderer))


class TestRenderer(unittest.TestCase):

    layer = COLLECTIVE_SHIBBOLETH_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.folder = api.content.create(
            container=self.portal,
            type="Folder",
            title="test"
        )

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)

        # TODO: Pass any default keywoard arguments to the Assignment constructor
        assignment = assignment or shibbolethloginportlet.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_render(self):
        # TODO: Pass any keywoard arguments to the Assignment constructor
        renderer = self.renderer(context=self.portal, assignment=shibbolethloginportlet.Assignment())
        renderer.update()
        # make sure to show the portlet
        renderer.show = True 
        output = renderer.render()
        # TODO: Test output
        self.assertIn("Institutional Login", output)


# def test_suite():
#     from unittest import TestSuite, makeSuite
#     suite = TestSuite()
#     suite.addTest(makeSuite(TestPortlet))
#     suite.addTest(makeSuite(TestRenderer))
#     return suite
