from django.contrib import admin
from django.conf import settings
from telegram import Bot

from .models import Category, Subcategory, Product, CartItem, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'subcategory', 'photo_link')
    list_filter = ('subcategory',)
    search_fields = ('name',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product', 'quantity')
    list_filter = ('user_id', 'product')
    search_fields = ('user_id', 'product__name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'creation_dttm', 'payment_amount', 'payment_link')
    list_filter = ('user_id', 'creation_dttm')
    search_fields = ('user_id__user', 'id')

    actions = ['send_email_to_clients']

    def send_telegram_message_to_clients(self, request, queryset):
        bot_token = settings.TG_BOT_TOKEN
        bot = Bot(token=bot_token)

        message = "Спасибо за ваш заказ! Мы работаем над его обработкой."

        for order in queryset:
            user_id = order.user_id
            if user_id:
                bot.send_message(chat_id=user_id, text=message)

        self.message_user(request, "Сообщения успешно отправлены через Telegram.")

    send_telegram_message_to_clients.short_description = "Отправить сообщение клиентам через Telegram"
