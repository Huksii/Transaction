from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from .utils import validate_phone_number
from django.forms import ValidationError

class Profile(models.Model):
    # username, first_name, last_name, email, password
    image = models.ImageField(upload_to='profile_images', blank=True, null=True, verbose_name='Аватарка',
        help_text='Загрузите фото вашего профиля')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', unique=True,
        help_text='Уникальный номер телефона', validators=[validate_phone_number])
    balance = models.PositiveBigIntegerField(default=0, verbose_name='Balance', help_text='Ваш баланс')
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text= 'Пользователь--Профиль')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    def __str__(self):
        return f'Profile: {self.user.username}'
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-created_at']

class Transaction(models.Model):
    # sender, receiver, amount, created_at
    sender_phone = models.CharField(max_length=20, verbose_name='Отправитель', validators=[validate_phone_number])
    receiver_phone = models.CharField(max_length=20, verbose_name='Получатель', validators=[validate_phone_number])
    amount = models.PositiveBigIntegerField(verbose_name='Сумма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    # До сохранения в базу данных можно проверить корректность данных
    def save(self, *args, **kwargs):
    # Встроенная функция save взаимодействует с базой данных
        try:
        # select all from profile where phone = self.sender_phone
            sender_profile = Profile.objects.get(phone=self.sender_phone)
        except Profile.DoesNotExist:
            return ValidationError('Отправитель не найден')
        if self.sender_phone == self.receiver_phone:
            return ValidationError('Нельзя перевести самому себе')
        try:
            receiver_profile = Profile.objects.get(phone=self.receiver_phone)
        except Profile.DoesNotExist:
            return ValidationError('Получатель не найден')
        if sender_profile.balance < self.amount:
            return ValidationError('Недостаточно средств')
        if self.amount <100:
            return ValidationError('Минимальная сумма перевода не меньше 100')
        sender_profile.balance -= self.amount
        receiver_profile.balance += self.amount
        sender_profile.save()
        receiver_profile.save()
        return super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.sender_phone} -> {self.receiver_phone} | сумма {self.amount}'
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']
        
class AddBalance(models.Model):
    # phone, amount, created_at
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', validators=[validate_phone_number])
    amount = models.PositiveBigIntegerField(verbose_name='Сумма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата пополнения')
    def save(self, *args, **kwargs):
        try:
            profile = Profile.objects.get(phone=self.phone)
        except Profile.DoesNotExist:
            return ValidationError('Пользователь не найден')
        if self.amount <100:
            return ValidationError('Минимальная сумма пополнения не меньше 100')
        profile.balance += self.amount
        profile.save()
        return super().save(*args, **kwargs)
    def __str__(self) -> str:
        return f'{self.phone} | сумма {self.amount}'
    class Meta:
        verbose_name = 'Пополнение баланса'
        verbose_name_plural = 'Пополнения баланса'
        ordering = ['-created_at']