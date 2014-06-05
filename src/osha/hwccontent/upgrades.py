# -*- coding: utf-8 -*-
from plone.app.contenttypes.migration.migration import DXEventMigrator
from plone.app.contenttypes.migration.migration import migrate
from plone.app.upgrade.utils import loadMigrationProfile


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
