from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer
from .models import Card
from .serializers import CardSerializer
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CardCreate(generics.CreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardList(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardRetrieve(generics.RetrieveAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardUpdate(generics.UpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardDelete(generics.DestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer



