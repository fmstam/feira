"""
    Permissions and Authentication helpers
"""

from guardian.shortcuts import assign_perm, get_objects_for_group
from django.contrib.auth import models as auth_models

class AuthenticationManager():
    """
    A helper class to manage the permissions and tokens
    """

    # group_name: [api.privilege, ...] dictionary
    group_permissions = {
                        "manager": ["api.create_dummy_lists", 
                                    "api.rebase_ml",
                                    "api.change_categories"],
                        "user": ["api.view_listing",
                                "api.change_listing"],
                        "guest": ["api.view_listing"]
                    }
    
    
    @classmethod
    def assing_permissions(cls, group_permissions_dict, 
                          assign_method=assign_perm # from guardian backend
                          ): 
        """
        Assing permissions to a group.

        :param group_permissions_dict: dictionary of format group:[permissions]
        :param assign_method: security backend method to manage permissions. 
            The default is ``guardian.shortcuts.assign_perm``

        """
        for group_name, permissions in group_permissions_dict:
            group = auth_models.Group.objects.get(name=group_name)
            for permission in permissions:
                assign_method(permission, group)

    @classmethod
    def has_permission(user, permissions, object):
        """
        Check if ``user`` has ``permissions`` on ``object``
        """
        
        for group in user.group.all():
            if get_objects_for_group(group=group, 
                    perms=permissions).filter(id=object.id).exists():
                return True

        return  False



