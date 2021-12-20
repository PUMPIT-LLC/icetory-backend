from django.db import models


# Menu


class Category(models.Model):
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title


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
    portion_unit = models.CharField(
        max_length=10, default="г.", verbose_name="Единица измерения порции"
    )

    def __str__(self):
        return self.title


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


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.SmallIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.product} - {self.amount} шт."


class Order(models.Model):
    name = models.CharField(max_length=120, verbose_name="Имя заказчика")
    phone = models.CharField(max_length=12, verbose_name="Телефон")
    email = models.EmailField(verbose_name="E-mail")

    address = models.CharField(max_length=255, verbose_name="Адрес")
    entrance = models.PositiveSmallIntegerField(verbose_name="Подъезд")
    apartment = models.PositiveIntegerField(verbose_name="Квартира")
    floor = models.PositiveSmallIntegerField(verbose_name="Этаж")
    comment = models.TextField(default="", verbose_name="Комментарий")
    intercom = models.BooleanField(default=True, verbose_name="Есть домофон?")

    day = models.DateField(verbose_name="День доставки")
    delivery_time = models.CharField(
        max_length=12, choices=DeliveryTime.choices, verbose_name="Время доставки"
    )
    payment_type = models.CharField(
        max_length=20, choices=PaymentType.choices, verbose_name="Способ оплаты"
    )

    items = models.ManyToManyField(CartItem, verbose_name="Позиции")

    def __str__(self):
        return f"Заказ {self.name} на {self.day} в период {self.delivery_time}"
