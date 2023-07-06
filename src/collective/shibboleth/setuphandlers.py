from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'collective.shibboleth:uninstall',
        ]


def setupVarious(context, site=None):
    """
    Set up various aspects of Plone that we can't set up using
    GenericSetup profiles (yet).  These aspects should be removed
        whenever possible and replaced with a GS import profile.
    """

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.shibboleth_various.txt') is None:
        return

    # Add additional setup code here
    site = site or getSite()

    # Manual install of AutoUserMakerPASPlugin
    qi = getToolByName(site, 'portal_quickinstaller')
    qi.installProduct('AutoUserMakerPASPlugin')


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.

    # Remove the roles defined.
    # Saidly there is no `rolemap.xml` removal for it
    # also there is no ZMI page to remove it,
    # thus we have to remove it manually here
    # based on Products/GenericSetup/rolemap.py
    roles_to_cleanup = [
        "Shibboleth Authenticated",
    ]
    portal = api.portal.get()
    ac_roles = getattr(portal, '__ac_roles__', [])
    cleaned_up_roles = list(filter(lambda x: x not in roles_to_cleanup, ac_roles))
    portal.__ac_roles__ = tuple(cleaned_up_roles)
