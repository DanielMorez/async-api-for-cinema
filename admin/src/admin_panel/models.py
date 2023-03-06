from django.db import models
from django.db.models import JSONField
from django.utils import timezone


class TemplateCodes(models.TextChoices):
    """Template codes."""

    common = 'common', 'Обычное письмо'
    monthly_personal_statistic = 'monthly_personal_statistic', 'Ежемесячная персональная статистика'


class Transport(models.TextChoices):
    sms = 'sms'
    email = 'email'


class Template(models.Model):
    """Email template."""

    title = models.CharField('Наименование', max_length=250)
    code = models.CharField(choices=TemplateCodes.choices, max_length=50)
    template = models.TextField()
    subject = models.TextField(blank=True, null=True)
    transport = models.CharField(choices=Transport.choices, max_length=50, default=Transport.email)

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """Save template."""
        if not self.id:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notification_templates'


class NotificationStatuses(models.TextChoices):
    to_send = 'pending', 'В очередь на отправку'
    done = 'done', 'Отправлено'
    cancelled = 'cancelled', 'Отменено'


class Priority(models.TextChoices):
    high = 'high', 'Высокий приоритет'
    medium = 'medium', 'Средний приоритет'
    low = 'low', 'Низкий приоритет'


class MailingTask(models.Model):
    """Model mailing task."""

    status = models.CharField(
        max_length=250,
        choices=NotificationStatuses.choices,
        default=NotificationStatuses.to_send,
    )

    is_promo = models.BooleanField(default=True)

    priority = models.CharField(
        max_length=250,
        choices=Priority.choices,
        default=Priority.low
    )
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)
    context = JSONField(default={})

    scheduled_datetime = models.DateTimeField(blank=True, null=True)
    execution_datetime = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """Save task."""
        if not self.id:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'mailing_tasks'
