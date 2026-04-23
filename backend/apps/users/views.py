from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    LoginSerializer,
    GoogleAuthSerializer,
    get_tokens_for_user
)
from .models import User


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create default budget and categories
        self._create_default_budget(user)

        # Generate JWT tokens
        tokens = get_tokens_for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)

    def _create_default_budget(self, user):
        """Create default budget with categories for new user"""
        from apps.budgets.models import Budget, BudgetMember
        from apps.categories.models import Category

        # Create default budget
        budget = Budget.objects.create(
            name='Основной',
            currency='RUB',
            author=user
        )

        # Add user as owner
        BudgetMember.objects.create(
            budget=budget,
            user=user,
            role='owner'
        )

        # Create default categories
        default_categories = [
            {'name': 'Продукты', 'icon_name': 'shopping_basket', 'color': '#0f6667'},
            {'name': 'Кафе', 'icon_name': 'restaurant', 'color': '#a53c00'},
            {'name': 'Досуг', 'icon_name': 'movie', 'color': '#2563eb'},
            {'name': 'Здоровье', 'icon_name': 'medical_services', 'color': '#dc2626'},
            {'name': 'Интернет', 'icon_name': 'language', 'color': '#7c3aed'},
            {'name': 'Электричество', 'icon_name': 'bolt', 'color': '#a16207'},
            {'name': 'Счета', 'icon_name': 'receipt_long', 'color': '#57534e'},
        ]

        for i, cat_data in enumerate(default_categories):
            Category.objects.create(
                budget=budget,
                name=cat_data['name'],
                icon_name=cat_data['icon_name'],
                color=cat_data['color'],
                sort_order=i,
                type='expense'
            )


class LoginView(APIView):
    """User login endpoint"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate JWT tokens
        tokens = get_tokens_for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': tokens
        })


class GoogleAuthView(generics.CreateAPIView):
    """Google OAuth authentication endpoint"""
    permission_classes = [AllowAny]
    serializer_class = GoogleAuthSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get or create user from Google token
        user = serializer.save()

        # Create default budget if user is new (check if user has any budgets as author)
        from apps.budgets.models import Budget
        if not Budget.objects.filter(author=user).exists():
            self._create_default_budget(user)

        # Generate JWT tokens
        tokens = get_tokens_for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': tokens
        })

    def _create_default_budget(self, user):
        """Create default budget with categories for new user"""
        from apps.budgets.models import Budget, BudgetMember
        from apps.categories.models import Category

        # Create default budget
        budget = Budget.objects.create(
            name='Основной',
            currency='RUB',
            author=user
        )

        # Add user as owner
        BudgetMember.objects.create(
            budget=budget,
            user=user,
            role='owner'
        )

        # Create default categories
        default_categories = [
            {'name': 'Продукты', 'icon_name': 'shopping_basket', 'color': '#0f6667'},
            {'name': 'Кафе', 'icon_name': 'restaurant', 'color': '#a53c00'},
            {'name': 'Досуг', 'icon_name': 'movie', 'color': '#2563eb'},
            {'name': 'Здоровье', 'icon_name': 'medical_services', 'color': '#dc2626'},
            {'name': 'Интернет', 'icon_name': 'language', 'color': '#7c3aed'},
            {'name': 'Электричество', 'icon_name': 'bolt', 'color': '#a16207'},
            {'name': 'Счета', 'icon_name': 'receipt_long', 'color': '#57534e'},
        ]

        for i, cat_data in enumerate(default_categories):
            Category.objects.create(
                budget=budget,
                name=cat_data['name'],
                icon_name=cat_data['icon_name'],
                color=cat_data['color'],
                sort_order=i,
                type='expense'
            )


class MeView(generics.RetrieveUpdateAPIView):
    """Get or update current user info"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
