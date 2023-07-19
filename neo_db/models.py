# neo_db/models.py
from django.db import models
from neomodel import StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty
from neo4j import GraphDatabase
from django.core.exceptions import ValidationError

class User(models.Model):
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)
    phone_num = models.CharField(max_length=20)
    user_photo = models.CharField(max_length=5000, blank=True, null=True)
    is_user = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
