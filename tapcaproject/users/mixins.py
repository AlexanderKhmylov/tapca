from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyMyDataMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return object == self.request.user
