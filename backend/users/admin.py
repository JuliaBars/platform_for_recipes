from django.contrib import admin

from users.models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_subscriber', 'get_author')
    search_fields = ('subscriber__email', 'author__email')

    @admin.display(description='Email подписчика')
    def get_subscriber(self, obj):
        return obj.subscriber.email

    @admin.display(description='Email автора')
    def get_author(self, obj):
        return obj.author.email
