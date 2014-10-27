# -*- coding: utf-8 -*-
from plone.app.contenttypes.migration.migration import DXEventMigrator
from plone.app.contenttypes.migration.migration import migrate
from plone.app.upgrade.utils import loadMigrationProfile
from plone.app.event.dx.behaviors import IEventLocation as IBaseEventLocation
from osha.hwccontent.behaviors.event import IEventLocation


def migrate_from_pa_event(context):
    loadMigrationProfile(context, 'profile-osha.hwccontent:default')
    # Re-import types to get newest Event type
    context.runImportStepFromProfile(
        'profile-osha.hwccontent:default',
        'typeinfo',
    )
    portal = context.getParentNode()
    migrate(portal, DXEventMigrator)


def install_content_rules(context):
    # install content rules
    context.runImportStepFromProfile(
        'profile-osha.hwccontent:default',
        'contentrules',
    )


def update_event_location(context):
    # Re-install Event and migrate the location field
    context.runImportStepFromProfile(
        'profile-osha.hwccontent:default',
        'typeinfo',
    )
    portal = context.getParentNode()
    results = portal.portal_catalog(portal_type="Event", Language="all")
    for res in results:
        event = res.getObject()
        old = IBaseEventLocation(event)
        new = IEventLocation(event)
        if not new.location:
            new.location = old.location
            event.reindexObject()

def install_jsregistry(context):
    context.runImportStepFromProfile('profile-osha.hwccontent:default', 'jsregistry',)
