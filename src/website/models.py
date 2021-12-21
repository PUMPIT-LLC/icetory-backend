from django.db import models

# pylint: disable=invalid-str-returned

NAME_MAX_LENGTH = 120
PHONE_MAX_LENGTH = 12

# Common Models


class CreatedDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        abstract = True


# Menu


class Category(models.Model):
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    categories = models.ManyToManyField(Category, verbose_name="Категории")

    title = models.CharField(max_length=120, verbose_name="Название")
    description = models.TextField(verbose_name="Состав/описание")

    weight = models.PositiveIntegerField(default=100, verbose_name="Вес (для БЖУ)")
    calories = models.PositiveIntegerField(verbose_name="Калории")
    proteins = models.PositiveSmallIntegerField(verbose_name="Белки")
    fats = models.PositiveSmallIntegerField(verbose_name="Жиры")
    carbs = models.PositiveSmallIntegerField(verbose_name="Углеводы")

    price = models.IntegerField(verbose_name="Цена")
    portion = models.PositiveIntegerField(verbose_name="Размер порции")
    portion_unit = models.CharField(max_length=10, default="г.", verbose_name="Единица измерения порции")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"


# Orders


class DeliveryTime(models.TextChoices):
    MORNING = "8-11", "8.00-11.00"
    MIDDAY = "11-14", "11.00-14.00"
    DAY = "14-17", "14.00-17.00"
    EVENING = "17-20", "17.00-20.00"


class PaymentType(models.TextChoices):
    CARD_ONLINE = "card-online", "Картой онлайн"
    CARD_OFFLINE = "card-offline", "Картой при получении"
    CASH = "cash", "Наличными"


class Order(CreatedDateModel):
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name="Имя заказчика")
    phone = models.CharField(max_length=PHONE_MAX_LENGTH, verbose_name="Телефон")
    email = models.EmailField(verbose_name="E-mail")

    address = models.CharField(max_length=255, verbose_name="Адрес")
    entrance = models.PositiveSmallIntegerField(verbose_name="Подъезд")
    apartment = models.PositiveIntegerField(verbose_name="Квартира")
    floor = models.PositiveSmallIntegerField(verbose_name="Этаж")
    comment = models.TextField(default="", verbose_name="Комментарий")
    intercom = models.BooleanField(default=True, verbose_name="Есть домофон?")

    day = models.DateField(verbose_name="День доставки")
    delivery_time = models.CharField(max_length=12, choices=DeliveryTime.choices, verbose_name="Время доставки")
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, verbose_name="Способ оплаты")

    def __str__(self):
        return f"Заказ {self.name} на {self.day} в период {self.delivery_time}"

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"


class CartItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.SmallIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.product} - {self.amount} шт."

    class Meta:
        verbose_name = "позиция заказа"
        verbose_name_plural = "позиции заказов"


# Feedback


class FeedbackComment(CreatedDateModel):
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name="Имя")
    phone = models.CharField(max_length=PHONE_MAX_LENGTH, verbose_name="Номер телефона")
    message = models.TextField(verbose_name="Отзыв")

    def __str__(self):
        return f"Отзыв от {self.name}"

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
