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


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        driver = GraphDatabase.driver("bolt://localhost:7689", auth=("neo4j", "12345678"))
        with driver.session() as session:
            session.run(
                "CREATE (:User {user_name: $user_name, password: $password, user_email: $user_email, "
                "phone_num: $phone_num, user_photo: $user_photo, is_user: $is_user, created_at: $created_at})",
                user_name=self.user_name, password=self.password, user_email=self.user_email,
                phone_num=self.phone_num, user_photo=self.user_photo, is_user=self.is_user, created_at=self.created_at
            )

