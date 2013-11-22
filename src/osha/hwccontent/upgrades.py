# -*- coding: utf-8 -*-
from plone.app.contenttypes.migration.migration import DXEventMigrator
from plone.app.contenttypes.migration.migration import migrate
from plone.app.upgrade.utils import loadMigrationProfile


def migrate_from_pa_event(context):
    loadMigrationProfile(context, 'profile-plone.app.event:default')
    # Re-import types to get newest Event type
    context.runImportStepFromProfile(
        'profile-plone.app.contenttypes:default',
        'typeinfo',
    )
    portal = context.getParentNode()
    migrate(portal, DXEventMigrator)