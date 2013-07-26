from django.contrib import admin
from game.models import Game, Organization, OrganizationMember, Rank


admin.site.register(Game)
admin.site.register(Rank)
admin.site.register(Organization)
admin.site.register(OrganizationMember)
