"""
    Permissions and Authentication helpers
"""

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class AuthTools():
    """
    A helper class to manage the permissions and tokens
    """

    ###### groups
    MANAGER = "manager"
    USER    = "user"

    ###### Premissions
    # listings
    VIEW_LISTING   = "fair.view_listing"
    CHANGE_LISTING = "fair.change_listing"
    DELETE_LISTING = "fair.delete_listing"

    # logs
    VIEW_ACTIVITY_LOG   = "fair.view_activity_log"
    CHANGE_ACTIVITY_LOG = "fair.change_activity_log"

    # ML 
    VIEW_DASHBOARD      = "fair.view_dashboard"
    RUN_DASHBOARD_TASKS      = "fair.view_dashboard"

    CHANGE_CATEGORIES     = "fair.change_categories"
    CREATE_DUMMY_LISTINGS = "fair.create_dummy_lists"

    
    # group_name: [api.privilege, ...] dictionary
    group_permissions = {
                        "manager": [VIEW_LISTING, 
                                    CHANGE_LISTING,
                                    DELETE_LISTING,
                                    VIEW_DASHBOARD,
                                    RUN_DASHBOARD_TASKS,
                                    # CHANGE_CATEGORIES,
                                    # CREATE_DUMMY_LISTINGS
                                    ],
                                    
                        "user": [VIEW_LISTING,
                                CHANGE_LISTING,
                                DELETE_LISTING],
    }
    
    @staticmethod
    def initialize(sender, **kwargs):
        
        # create permissions for dashboard
        # via modeless permission objects
        content_type = ContentType.objects.get_for_model(Permission)

        # dashboard permissions
        Permission.objects.create(content_type=content_type,
                                  name='view dashboard', codename='VIEW_DASHBOARD',)

        Permission.objects.create(content_type=content_type,
                                  name='run a dashboard task', codename='RUN_DASHBOARD_TASKS',)

        AuthTools.assign_permissions(AuthTools.group_permissions)


    @staticmethod
    def assign_permissions (group_permissions_dict): 
        """
        Assing permissions to a group.

        :param: group_permissions_dict: dictionary of format group:[permissions]
        """
        from guardian.shortcuts import assign_perm
        from django.contrib.auth import models as auth_models

        for group_name, permissions in group_permissions_dict.items():
            group = auth_models.Group.objects.get(name=group_name)
            for permission in permissions:
                assign_perm(permission, group)



    @staticmethod
    def group_has_permission(group, permissions, object):
        """
        Check if ``group`` has ``permissions`` on ``object``
        """
        from guardian.shortcuts import get_objects_for_group

        return get_objects_for_group(group=group, 
                    perms=permissions).filter(id=object.id).exists()

    @staticmethod
    def user_has_group_permission(user, permissions, object):
        """
        Check if ``user`` belongs to a group that has ``permissions`` on ``object``
        """

        for group in user.groups.all():
            if AuthTools.group_has_permission(group, permissions, object):
                return True
        
        return False