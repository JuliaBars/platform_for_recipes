from rest_framework.permissions import SAFE_METHODS, BasePermission


# Класс не по тз. Нет требований, чтобы был админский доступ через апи
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_staff)

# Класс избыточек, т.к. содержит в себе реализацию встроенного в DRF класса IsAuthenticatedOrReadOnly
class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


# Случилось затенение имен. См коммент выше.
class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # ИМХО, каст в bool тут лищний
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )
    # В таком виде не имеет смысла, т.к. этот метод будет вызван после того, как has_permission вернет True.
    # Так что, тут по любому уже есть безопасный запрос
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS
