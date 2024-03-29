from django.db import IntegrityError
from django.db.models import Avg
from django.db.models.functions import Round
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (IsAdminAsDefinedByUserModel,
                          IsAdminOrModeratorOrAuthorOrReadOnly,
                          IsAdminUserOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          CurrentUserSerializer, GenreSerializer,
                          ReadTitleSerializer, ReviewSerializer,
                          SignUpSerializer, TokenRequestSerializer,
                          UserSerializer, WriteTitleSerializer)
from .services import confirmation_email, generate_confirmation_code


class RubricBaseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Базовый вьюсет для категорий и жанров."""
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Создание и изменение рецензий."""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAdminOrModeratorOrAuthorOrReadOnly
    )

    def get_title(self):
        """Вывод произведения."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Вывод всех рецензий к определенному произведению."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создание рецензии."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Создание и изменение комментарий."""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAdminOrModeratorOrAuthorOrReadOnly
    )

    def get_review(self):
        """Вывод рецензии."""
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Вывод всех комментариев для определенной рецензии."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создание комментария."""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class CategoryViewSet(RubricBaseViewSet):
    """Создание и изменения категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(RubricBaseViewSet):
    """Создание и изменения жанра."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Создание и изменения произведения."""
    queryset = (
        Title.objects.annotate(rating=Round(Avg('reviews__score')))
    )
    ordering = ('name',)
    serializer_class = WriteTitleSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Вызов нужного сериализатора: для записи или для чтения."""
        if self.action in ['create', 'update', 'partial_update']:
            return WriteTitleSerializer
        return ReadTitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Создание или изменение пользователя."""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsAdminAsDefinedByUserModel,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_object(self):
        if self.action == 'me':
            return self.request.user
        return super().get_object()

    @action(
        methods=['GET', 'PATCH'], detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=CurrentUserSerializer
    )
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        raise MethodNotAllowed(request.method)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрация пользователя и отправка кода подтверждения."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(
            defaults={'is_active': False},
            **serializer.validated_data
        )
    except IntegrityError:
        return HttpResponseBadRequest(
            'Пользователь с таким именем или адресом уже существует'
        )
    user.code = generate_confirmation_code()
    user.save()
    confirmation_email(user.email, user.code)
    return Response({"email": user.email, "username": user.username})


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Проверка кода подтверждения."""
    serializer = TokenRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    confirmation_code = serializer.validated_data['confirmation_code']
    if confirmation_code != user.code:
        return HttpResponseBadRequest('Неверный код подтверждения')
    user.is_active = True
    user.save()
    return Response({'token': str(RefreshToken.for_user(user).access_token)})
