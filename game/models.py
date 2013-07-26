from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class GameManager(models.Manager):
    def get_latest(self):
        return self.get_query_set().order_by('-date')[:20]


class Game(models.Model):
    winner = models.ForeignKey(User, related_name='games_won')
    loser = models.ForeignKey(User, related_name='games_lost')
    date = models.DateTimeField(default=datetime.now)

    objects = GameManager()

    def clean(self):
        if (self.winner_id is not None and self.loser_id is not None and
                self.winner_id == self.loser_id):
            raise ValidationError(
                'Winner and loser can\'t be the same person!'
            )

    def __unicode__(self):
        return '%s beats %s' % (
            self.winner,
            self.loser
        )

    def __str__(self):
        return self.__unicode__()


class RankManager(models.Manager):
    def get_score_board(self):
        return self.get_query_set().order_by('-rank')


class Rank(models.Model):
    user = models.ForeignKey(User, related_name='rank', unique=True)
    rank = models.IntegerField(default=1000)
    stdev = models.FloatField('standard deviation', default=50)

    objects = RankManager()

    def __unicode__(self):
        return '%s (%d/%d)' % (
            self.user.username,
            self.rank,
            self.stdev
        )

    def __str__(self):
        return self.__unicode__()


class Organization(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='organizations',
                                     through='OrganizationMember')

    def __unicode__(self):
        return self.name


class OrganizationMember(models.Model):
    STATUS_MEMBER = 0
    STATUS_ADMINISTRATOR = 1

    STATUSES = (
        (STATUS_MEMBER, _('Member')),
        (STATUS_ADMINISTRATOR, _('Administrator')),
    )

    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)
    status = models.PositiveSmallIntegerField(choices=STATUSES,
                                              default=STATUS_MEMBER)

    class Meta:
        unique_together = (
            ('user', 'organization'),
        )

    def __unicode__(self):
        return _('%s member of %s') % (
            self.user.username,
            self.organization.name
        )
