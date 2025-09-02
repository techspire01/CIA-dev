from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils import timezone
import datetime
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    is_critical = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    referral_url = models.URLField(max_length=500, blank=True, null=True)
    image1 = models.ImageField(upload_to="announcements/images/", blank=True, null=True)
    image2 = models.ImageField(upload_to="announcements/images/", blank=True, null=True)
    image3 = models.ImageField(upload_to="announcements/images/", blank=True, null=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"

class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)  # enforce unique name  
    founder_name = models.CharField(max_length=255, blank=True, null=True)

    website_url = models.URLField(max_length=500, blank=True, null=True)
    logo = models.ImageField(upload_to="suppliers/logos/", blank=True, null=True)
    image = models.ImageField(upload_to="suppliers/images/", blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    sub_category1 = models.CharField(max_length=255, blank=True, null=True)
    sub_category2 = models.CharField(max_length=255, blank=True, null=True)
    sub_category3 = models.CharField(max_length=255, blank=True, null=True)
    sub_category4 = models.CharField(max_length=255, blank=True, null=True)
    sub_category5 = models.CharField(max_length=255, blank=True, null=True)
    sub_category6 = models.CharField(max_length=255, blank=True, null=True)
    product_image1 = models.ImageField(upload_to="suppliers/product_images/", blank=True, null=True)
    product_image2 = models.ImageField(upload_to="suppliers/product_images/", blank=True, null=True)
    product_image3 = models.ImageField(upload_to="suppliers/product_images/", blank=True, null=True)
    product_image4 = models.ImageField(upload_to="suppliers/product_images/", blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    contact_person_name = models.CharField(max_length=255, blank=True, null=True)
    person_image = models.ImageField(upload_to="suppliers/person_images/", blank=True, null=True)

    # Product fields
    product1 = models.CharField(max_length=255, blank=True, null=True)
    product2 = models.CharField(max_length=255, blank=True, null=True)
    product3 = models.CharField(max_length=255, blank=True, null=True)

    # Split address fields
    door_number = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)

    # Expanded business details
    business_description = models.TextField(blank=True, null=True)

    phone_number = models.CharField(max_length=15, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    cia_id = models.PositiveIntegerField(unique=True, blank=True, null=True)  # CIA serial id

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.cia_id:
            # Assign next available cia_id (serialized, no gaps)
            existing_ids = Supplier.objects.exclude(pk=self.pk).order_by('cia_id').values_list('cia_id', flat=True)
            next_id = 1
            for eid in existing_ids:
                if eid != next_id:
                    break
                next_id += 1
            self.cia_id = next_id
        super().save(*args, **kwargs)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        swappable = 'AUTH_USER_MODEL'

class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to="team/images/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    linkedin_url = models.URLField(max_length=500, blank=True, null=True)
    twitter_url = models.URLField(max_length=500, blank=True, null=True)
    instagram_url = models.URLField(max_length=500, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.position}"

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + datetime.timedelta(minutes=10)

class PhotoGallery(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="gallery/photos/")
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True, help_text="Optional category for organizing photos")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Photo Gallery"
        verbose_name_plural = "Photo Gallery"

    def __str__(self):
        return self.title

class PhotoGalleryImage(models.Model):
    photo_gallery = models.ForeignKey(PhotoGallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="gallery/photos/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Photo Gallery Image"
        verbose_name_plural = "Photo Gallery Images"

    def __str__(self):
        return f"Image for {self.photo_gallery.title} - {self.caption or 'No Caption'}"

class NewsGallery(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="gallery/news/")
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now, help_text="Date when the news item occurred")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-date']
        verbose_name = "News Gallery"
        verbose_name_plural = "News Gallery"

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"

class NewsGalleryImage(models.Model):
    news_gallery = models.ForeignKey(NewsGallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="gallery/news/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "News Gallery Image"
        verbose_name_plural = "News Gallery Images"

    def __str__(self):
        return f"Image for {self.news_gallery.title} - {self.caption or 'No Caption'}"
