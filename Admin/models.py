from django.db import models
from django.contrib.auth.hashers import make_password


class Roles(models.Model):
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'rolestable'

    def save(self, *args, **kwargs):
        if not self.id:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Students(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255)
    roll_number = models.IntegerField()
    email_id = models.EmailField(max_length=255)

    class Meta:
        db_table = 'studentstable'


class FeeCategories(models.Model):
    fee_choices = (
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('onetime', 'One-Time'),
    )
    name = models.CharField(max_length=100)
    fee_type = models.CharField(
        max_length=10,
        choices=fee_choices,
        default='monthly',  # You can set a default if needed
    )

    class Meta:
        db_table = 'feecategorytable'


class StudentFeesStatus(models.Model):
    fee_status = [
        ('Paid', 'Paid'),
        ('Due', 'Due'),
    ]
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    fee_category = models.ForeignKey(FeeCategories, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=fee_status, default='Due')
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'feestatus'

    def __str__(self):
        return f'{self.student.first_name} - {self.fee_category.name} - {self.status}'
