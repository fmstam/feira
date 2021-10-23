"""
    Permissions and Authentication helpers
"""


from datetime import timedelta, timezone


class AuthenticationManager():
    """
    A helper class to manage the permissions and tokens
    """

    # premissions

    # listings
    VIEW_LISTING = "fair.view_listing"
    CHANGE_LISTING = "fair.change_listing"
    DELETE_LISTING = "fair.change_listing"

    # logs
    VIEW_ACTIVITY_LOG = "api.view_activity_log"
    CHANGE_ACTIVITY_LOG = "api.change_activity_log"

    # ML 
    REBASE_ML = "api.rebase_ml"
    CHANGE_CATEGORIES = "api.change_categories"
    CREATE_DUMMY_LISTINGS = "api.create_dummy_lists"

    
    # group_name: [api.privilege, ...] dictionary
    group_permissions = {
                        "manager": [VIEW_LISTING, 
                                    CHANGE_LISTING,
                                    DELETE_LISTING],
                                    
                        "user": [VIEW_LISTING,
                                CHANGE_LISTING,
                                DELETE_LISTING],
    }
    
    @staticmethod
    def initialize(cls, sender, **kwargs):
        cls.assign_permissions(cls.group_permissions)
   
    @staticmethod
    def assign_permissions(cls, 
                         group_permissions_dict): 
        """
        Assing permissions to a group.

        :param group_permissions_dict: dictionary of format group:[permissions]
        """
        from guardian.shortcuts import assign_perm
        from django.contrib.auth import models as auth_models

        for group_name, permissions in group_permissions_dict.items():
            print(group_name)
            group = auth_models.Group.objects.get(name=group_name)
            for permission in permissions:
                assign_perm(permission, group)



    @staticmethod
    def group_has_permission(group, permissions, object):
        """
        Check if ``user`` has ``permissions`` on ``object``
        """
        from django.contrib.auth import get_objects_for_group

        
        return get_objects_for_group(group=group, 
                    perms=permissions).filter(id=object.id).exists()

    
     



