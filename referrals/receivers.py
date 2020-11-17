from .models import Link, Referral
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from .signals import create_referral
from .utils import validate_uuid4
import logging

User = get_user_model()

logger = logging.getLogger(__name__)

@receiver(create_referral, sender=User)
def save_referral(sender, request, user, position, **kwargs):
    if position is not 'child' and position is not 'sibling':
        logger.exception('{} was sent instead of a child or brother'.format(
            position))  # pragma: no cover
        raise KeyError('Position can be child or sibling')  # pragma: no cover

    referral_link = request.POST.get('referral', None)
    if not referral_link:
        referral_link = request.GET.get('ref', None)
    try:
        if validate_uuid4(referral_link):
            link = Link.objects.get(token=referral_link)
            try:
                referral = Referral.objects.get(user=link.user)
                if position == 'sibling':
                    referral.add_sibling(user=user)
                else:
                    referral.add_child(user=user)
            except Referral.DoesNotExist:  # pragma: no cover
                logger.exception(
                    'Referral with user = {} does not exist'.format(
                        link.user
                    )
                )
    except Link.DoesNotExist:  # pragma: no cover
        logger.exception(
            'Link with token = {} does not exist'.format(referral_link))
    except ValidationError:  # pragma: no cover
        logger.exception('{} is not a valid Link.token'.format(referral_link))
