from django.db import models

# Create your models here.
class Participant(models.Model):
    telegram_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=32, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    is_banned = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    balance = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    is_premium = models.BooleanField(default=False)
    skills_list = models.ManyToManyField(Skill, blank=True)
    certificates = models.ManyToManyField(Certificate, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.URLField(null=True, blank=True) # Еркебулан потом надо изменить на ImageField
    bio = models.CharField(null=True, blank=True, max_length=60)
    is_verified = models.BooleanField(default=False)
    achievements = models.ManyToManyField(Achievement, blank=True)
    hackathons = models.ManyToManyField(Hackathon, blank=True)
    friends = models.ManyToManyField('self', blank=True) # Еркебулан потом надо посмотреть, как сделать друзей
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, null=True, blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    THEME_CHOICES = [
        ('dark', 'Темный'),
        ('light', 'Светлый'),
    ]

    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'Английский'),
    ]

    # Функции для подсчета уровня
    def calculate_level(self):
        """Подсчет текущего уровня и обновление"""
        xp = self.xp
        level = 1
        required_xp = 0

        while xp >= required_xp:
            level += 1
            required_xp = 100 + (level - 2) * 50  # 100 для уровня 2, +50 для каждого следующего

        self.level = level - 1  # Устанавливаем последний достигнутый уровень
        self.save()

    # Функция для подсчета количества XP для следующего уровня
    def get_next_level_xp(self):
        """XP, необходимое для следующего уровня"""
        return 100 + (self.level - 1) * 50

    # Функция для подсчета количества XP для текущего уровня
    def get_current_level_xp(self):
        """XP, необходимое для текущего уровня"""
        if self.level == 1:
            return 0
        return 100 + (self.level - 2) * 50

    # Функция для подсчета количества хакатонов
    def hackathon_count(self):
        return self.hackathons.count()
    
    # Функция для вывода имени пользователя
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.telegram_id}"

class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Certificate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name
    
class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name
