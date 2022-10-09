from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import username_validator, validator_year

from .mixins import ValidateUsernameMixin


class CurrentTitleDefault:
    """Сериализатор для модели произведения."""
    requires_context = True

    def __call__(self, serializer_field):
        return (
            serializer_field.context.get('request')
            .parser_context.get('kwargs').get('title_id')
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для рецензий."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=CurrentTitleDefault())

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Вы уже оставили отзыв, спасибо!'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class RubricSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для сущностей с именем и кодом."""
    class Meta:
        fields = ('name', 'slug')


class CategorySerializer(RubricSerializer):
    """Сериализатор для категорий."""

    class Meta(RubricSerializer.Meta):
        model = Category


class GenreSerializer(RubricSerializer):
    """Сериализатор для жанров."""

    class Meta(RubricSerializer.Meta):
        model = Genre


class WriteTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для сохранения произведения."""
    year = serializers.IntegerField(
        validators=[validator_year()],
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )


class ReadTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода произведения."""
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = ('__all__',)


class UserSerializer(ValidateUsernameMixin, serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class CurrentUserSerializer(UserSerializer):
    """Дополнительный сериализатор для User с ограничением."""
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(ValidateUsernameMixin, serializers.Serializer):
    """Сериализатор для регистрации пользователя."""
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150, validators=(username_validator(),)
    )


class TokenRequestSerializer(serializers.Serializer):
    """Сериализатор для запроса токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()
