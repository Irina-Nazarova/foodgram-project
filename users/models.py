from django.contrib.auth.models import AbstractUser
from django.db import models
#
#
# class UserRole(models.TextChoices):
#     """
#     The Role entries are managed by the system,
#     automatically created via a Django data migration.
#     """
#
#     ADMIN = ('admin', 'admin',)
#     USER = ('user', 'user',)
#
#
# class User(AbstractUser):
#     """
#     Creating the custom User model
#     based on the AbstractUser model
#     """
#     # bio = models.TextField(blank=True, null=True)
#     # role = models.CharField(
#     #     max_length=150,
#     #     blank=False,
#     #     choices=UserRole.choices,
#     #     default=UserRole.USER,
#     # )
#     bio = models.TextField(max_length=200,
#                            blank=True,
#                            verbose_name="user\'s biography",
#                            help_text="Here You add Your bio")
#
#     role = models.CharField(choices=UserRole.choices,
#                             default=UserRole.USER,
#                             max_length=40,
#                             verbose_name="user\'s role")
#
#     email = models.EmailField(blank=False, unique=True)
#
#     username = models.CharField(  max_length=150, blank=True, null=True, unique=True, db_index=True)
#
#     # confirmation_code = models.CharField(
#     #     max_length=150,
#     #     blank=True,
#     #     null=True,
#     # )
#
#     password = models.CharField(max_length=255, blank=False, null=True)
#
#     #date_joined = models.DateTimeField(blank=True, null=True)
#
#     first_name = models.TextField(max_length=30, blank=True, null=True)
#     last_name = models.TextField(max_length=30, blank=True, null=True)
#
#     # class Meta:
#     #     db_table = "users"
#
#     @property
#     def is_admin(self):
#         return self.role == "admin" or self.is_staff
#
#     class Meta(AbstractUser.Meta):
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
#         ordering = ['id']
#     #
#     # def __str__(self):
#     #     return self.username