import random
import string
from django.utils import timezone
from django.utils.text import slugify

########## JSON WEB TOKEN ##########
def jwt_response_payload_handler(token, user):
    data = {
        "token": token,
        "user": user.id,
        "orig_iat": timezone.now(),
    }
    return data

########## RANDOM STRING GENERATOR ##########
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

###############  REFERRAL RANDOM STRING GENERATOR   ###############
def referral_random_string_generator(size = 10, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

###############  TRANSACTION RANDOM STRING GENERATOR   ###############
def random_transaction_id_generator(size = 20, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

###############   UNIQUE REFERRAL ID GENERATOR   ###############
def unique_referral_id_generator(instance):
    referral_new_id = referral_random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(referral_id = referral_new_id).exists()
    if qs_exists:
        return unique_referral_id_generator(instance)
    return referral_new_id

########## UNIQUE SLUG GENERATOR ##########
def unique_slug_generator(instance, new_slug = None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug = slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug = slug,
            randstr = random_string_generator(size = 4)
        )
        return unique_slug_generator(instance, new_slug = new_slug)
    return slug

###############   UNIQUE TRANSACTION ID GENERATOR   ###############
def unique_transaction_id_generator(instance):
    transaction_new_id = random_transaction_id_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(transaction_id = transaction_new_id).exists()
    if qs_exists:
        return random_transaction_id_generator(instance)
    return transaction_new_id