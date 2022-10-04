from random import randint

from django.core.cache import cache
from templated_mail.mail import BaseEmailMessage


class ActivationEmail(BaseEmailMessage):
    template_name = "email/activation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = context.get("user")

        random_number = randint(0, 9999)
        activation_code = str(random_number)
        while len(activation_code) < 4:
            activation_code = "0" + activation_code

        cache.set(
            f"tasks_backend:activation_codes:{user.pk}", activation_code, timeout=60 * 3
        )

        context["activation_code"] = activation_code
        return context
