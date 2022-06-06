from django.db import models
from .services import AccountServices
from _helpers import CacheService

DOWNLOAD_EXPIRATION = 60 * 60 * 24


class Account(models.Model):
    email = models.EmailField(max_length=300)
    password = models.CharField(max_length=300)

    @staticmethod
    def get_first_available_account():
        service: CacheService = CacheService()
        for account in Account.objects.all():
            if int(service.get_from_redis(key=account.email).decode()) < 2:
                return account

    def download_vector(self, data_id: int, extension='png'):
        service = AccountServices()
        cache_service: CacheService = CacheService()

        download_auth = service.get_download_auth(self.email)
        download_link = service.get_download_link(download_auth, data_id, extension)
        cache_service.incr_from_redis(key=self.email, ttl=DOWNLOAD_EXPIRATION)

        return download_link
