from django.db import models

# pylint: disable=invalid-str-returned

NAME_MAX_LENGTH = 120
PHONE_MAX_LENGTH = 12

# Common Models


class CreatedDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        abstract = True


# Marketing content


class VideoStory(models.Model):
    predefined_id = models.PositiveSmallIntegerField(verbose_name="Идентификатор (порядковый номер)")
    url = models.URLField(verbose_name="Ссылка на видео")

    def __str__(self):
        return str(self.predefined_id)

    class Meta:
        verbose_name = "стори"
        verbose_name_plural = "стори"


class ClientReview(models.Model):
    first_name = models.CharField(max_length=120, verbose_name="Имя")
    last_name = models.CharField(max_length=120, verbose_name="Фамилия")
    photo = models.ImageField(upload_to="reviews", verbose_name="Фото")
    review = models.TextField(verbose_name="Текст отзыва")

    def __str__(self):
        return f"Отзыв от {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "отзыв (карточка на сайте)"
        verbose_name_plural = "отзывы (сайт)"


# Menu


class Category(models.Model):
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class ProductImage(models.Model):
    title = models.CharField(max_length=120, blank=True, default="", verbose_name="Символическое название")
    image = models.ImageField(upload_to="products", verbose_name="Изображение")

    def __str__(self):
        return self.title if self.title else self.image.name

    class Meta:
        verbose_name = "изображение блюда"
        verbose_name_plural = "изображения блюд"


class Product(models.Model):
    primary_category = models.ForeignKey(
        Category, verbose_name="Главная категория", related_name="primary_category", on_delete=models.PROTECT
    )
    secondary_categories = models.ManyToManyField(
        Category, verbose_name="Второстепенные категории", related_name="secondary_categories"
    )

    title = models.CharField(max_length=120, verbose_name="Название")
    description = models.TextField(verbose_name="Состав/описание")

    calories = models.PositiveIntegerField(verbose_name="Калории")
    proteins = models.PositiveSmallIntegerField(verbose_name="Белки")
    fats = models.PositiveSmallIntegerField(verbose_name="Жиры")
    carbs = models.PositiveSmallIntegerField(verbose_name="Углеводы")

    price = models.IntegerField(verbose_name="Цена")
    discount_price = models.IntegerField(
        null=True,
        default=None,
        blank=True,
        verbose_name="Цена по скидке",
        help_text="Оставьте пустым, чтобы скидка не выводилась",
    )
    portion = models.PositiveIntegerField(verbose_name="Размер порции")
    portion_unit = models.CharField(max_length=10, default="г.", verbose_name="Единица измерения порции")

    main_picture = models.ForeignKey(ProductImage, related_name="main_picture", on_delete=models.PROTECT)
    extra_picture = models.ForeignKey(ProductImage, related_name="extra_picture", on_delete=models.PROTECT)

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


class OrderStatus(models.IntegerChoices):
    SPAM = -1, "Спам"
    CREATED = 0, "Создан"
    IN_PROGRESS = 10, "Взят в работу"
    DONE = 20, "Готов"


class Order(CreatedDateModel):
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name="Имя заказчика")
    phone = models.CharField(max_length=PHONE_MAX_LENGTH, verbose_name="Телефон")
    email = models.EmailField(verbose_name="E-mail")

    address = models.CharField(max_length=255, verbose_name="Адрес")
    entrance = models.PositiveSmallIntegerField(null=True, default=None, blank=True, verbose_name="Подъезд")
    apartment = models.PositiveIntegerField(verbose_name="Квартира")
    floor = models.PositiveSmallIntegerField(verbose_name="Этаж")
    comment = models.TextField(default="", verbose_name="Комментарий")
    intercom = models.CharField(max_length=60, default="", verbose_name="Есть домофон?")

    day = models.DateField(verbose_name="День доставки")
    delivery_time = models.CharField(max_length=12, choices=DeliveryTime.choices, verbose_name="Время доставки")
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, verbose_name="Способ оплаты")

    status = models.SmallIntegerField(default=OrderStatus.CREATED.value, choices=OrderStatus.choices)

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
