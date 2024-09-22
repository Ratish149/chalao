from django.db import models

# Create your models here.
class AppReview(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='app_reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} Reviewed on {self.created_at}'