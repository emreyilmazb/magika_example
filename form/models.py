from django.db import models

class JobApplication(models.Model):
    POSITIONS = [
        ('developer', 'Backend Developer'),
        ('designer', 'UI/UX Designer'),
        ('manager', 'Project Manager'),
    ]

    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=15, verbose_name="Phone Number")
    position = models.CharField(max_length=50, choices=POSITIONS, verbose_name="Position Applied For")
    cv = models.FileField(upload_to='cv/', verbose_name="Upload Resume (PDF)")
    photo = models.ImageField(upload_to='photos/', verbose_name="Upload Photo")
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="Application Date")

    def __str__(self):
        return f"{self.name} - {self.position}"