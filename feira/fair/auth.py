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
    
    @classmethod
    def initialize(cls, sender, **kwargs):
        cls.assign_permissions(cls.group_permissions)

    @classmethod
    def create_access_token(cls, user):
        import oauth2_provider.models
        Application = oauth2_provider.models.get_application_model()
        AccessToken = oauth2_provider.models.get_access_token_model()
        token_expiration_time = timezone.now() + timedelta(minutes=60)
        token = AccessToken.objects.create(
            user=user,
            scope='read write packages',
            token='test{}{}'.format(
                user.id,
                int(token_expiration_time.timestamp()),
            ),
            application=Application.objects.first(),
            expires=token_expiration_time,
        )
        return token

    @classmethod
    def auth_header(cls, token):
        return { 'HTTP_AUTHORIZATION': 'Bearer {}'.format(token) }        
    
    @classmethod
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



