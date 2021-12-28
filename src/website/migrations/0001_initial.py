# Generated by Django 4.0 on 2021-12-28 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='ClientReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=120, verbose_name='Фамилия')),
                ('photo', models.ImageField(upload_to='reviews', verbose_name='Фото')),
                ('review', models.TextField(verbose_name='Текст отзыва')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
            },
        ),
        migrations.CreateModel(
            name='FeedbackComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('name', models.CharField(max_length=120, verbose_name='Имя')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('message', models.TextField(verbose_name='Отзыв')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('name', models.CharField(max_length=120, verbose_name='Имя заказчика')),
                ('phone', models.CharField(max_length=12, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('entrance', models.PositiveSmallIntegerField(blank=True, default=None, null=True, verbose_name='Подъезд')),
                ('apartment', models.PositiveIntegerField(verbose_name='Квартира')),
                ('floor', models.PositiveSmallIntegerField(verbose_name='Этаж')),
                ('comment', models.TextField(default='', verbose_name='Комментарий')),
                ('intercom', models.CharField(default='', max_length=60, verbose_name='Есть домофон?')),
                ('day', models.DateField(verbose_name='День доставки')),
                ('delivery_time', models.CharField(choices=[('8-11', '8.00-11.00'), ('11-14', '11.00-14.00'), ('14-17', '14.00-17.00'), ('17-20', '17.00-20.00')], max_length=12, verbose_name='Время доставки')),
                ('payment_type', models.CharField(choices=[('card-online', 'Картой онлайн'), ('card-offline', 'Картой при получении'), ('cash', 'Наличными')], max_length=20, verbose_name='Способ оплаты')),
                ('status', models.SmallIntegerField(choices=[(-1, 'Спам'), (0, 'Создан'), (10, 'Взят в работу'), (20, 'Готов')], default=0)),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=120, verbose_name='Символическое название')),
                ('image', models.ImageField(upload_to='products', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'изображение блюда',
                'verbose_name_plural': 'изображения блюд',
            },
        ),
        migrations.CreateModel(
            name='VideoStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predefined_id', models.PositiveSmallIntegerField(verbose_name='Идентификатор (порядковый номер)')),
                ('url', models.URLField(verbose_name='Ссылка на видео')),
            ],
            options={
                'verbose_name': 'стори',
                'verbose_name_plural': 'стори',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Состав/описание')),
                ('calories', models.PositiveIntegerField(verbose_name='Калории')),
                ('proteins', models.PositiveSmallIntegerField(verbose_name='Белки')),
                ('fats', models.PositiveSmallIntegerField(verbose_name='Жиры')),
                ('carbs', models.PositiveSmallIntegerField(verbose_name='Углеводы')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('discount_price', models.IntegerField(default=None, help_text='Оставьте пустым, чтобы скидка не выводилась', null=True, verbose_name='Цена по скидке')),
                ('portion', models.PositiveIntegerField(verbose_name='Размер порции')),
                ('portion_unit', models.CharField(default='г.', max_length=10, verbose_name='Единица измерения порции')),
                ('extra_picture', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='extra_picture', to='website.productimage')),
                ('main_picture', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='main_picture', to='website.productimage')),
                ('primary_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='primary_category', to='website.category', verbose_name='Главная категория')),
                ('secondary_categories', models.ManyToManyField(related_name='secondary_categories', to='website.Category', verbose_name='Второстепенные категории')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.SmallIntegerField(verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='website.product')),
            ],
            options={
                'verbose_name': 'позиция заказа',
                'verbose_name_plural': 'позиции заказов',
            },
        ),
    ]
