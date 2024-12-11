from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyMyDataMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user
