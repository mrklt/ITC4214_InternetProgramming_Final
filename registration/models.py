from django.db import models

from django.contrib.auth.models import User

def user_is_creator(self):
    return self.groups.filter(name='Creator').exists()

# Add the property dynamically to the User model
User.add_to_class('is_creator', property(user_is_creator))
