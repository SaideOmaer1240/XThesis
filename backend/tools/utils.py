from django.contrib.auth import get_user_model
class UserName:
    def __init__(self):
        self.User = get_user_model()
    def get_user_by_id(self, user_id):
        try:
            return self.User.objects.get(id=user_id)
        except self.User.DoesNotExist:
            return None
    