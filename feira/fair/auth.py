"""
    Permissions and Authentication helpers
"""



class AuthenticationManager():
    """
    A helper class to manage the permissions and tokens
    """

    # premissions

    # listings
    VIEW_LISTING = "api.view_listing"
    CHANGE_LISTING = "api.change_listing"

    # logs
    VIEW_ACTIVITY_LOG = "api.view_activity_log"
    CHANGE_ACTIVITY_LOG = "api.change_activity_log"

    # ML 
    REBASE_ML = "api.rebase_ml"
    CHANGE_CATEGORIES = "api.change_categories"
    CREATE_DUMMY_LISTINGS = "api.create_dummy_lists"

    
    # group_name: [api.privilege, ...] dictionary
    group_permissions = {
                        "manager": [CHANGE_CATEGORIES, 
                                    CHANGE_CATEGORIES,
                                    CREATE_DUMMY_LISTINGS],
                                    
                        "user": [VIEW_LISTING,
                                CHANGE_LISTING],

                        "guest": [VIEW_LISTING]
    }
    
    @classmethod
    def initialize(cls):
        
        

    @classmethod
    def assing_permissions(cls, 
                         group_permissions_dict): 
        """
        Assing permissions to a group.

        :param group_permissions_dict: dictionary of format group:[permissions]
        """
        from guardian.shortcuts import assign_perm
        from django.contrib.auth import models as auth_models

        for group_name, permissions in group_permissions_dict:
            group = auth_models.Group.objects.get(name=group_name)
            for permission in permissions:
                assign_perm(permission, group)

    @classmethod
    def has_permission(user, permissions, object):
        """
        Check if ``user`` has ``permissions`` on ``object``
        """
        from django.contrib.auth import get_objects_for_group
        for group in user.group.all():
            if get_objects_for_group(group=group, 
                    perms=permissions).filter(id=object.id).exists():
                return True

        return  False



