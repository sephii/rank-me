from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .forms import GameForm
from .models import Game, Rank


def index(request):
    latest_results = Game.objects.get_latest()
    score_board = Rank.objects.get_score_board()
    context = {
        'latest_results': latest_results,
        'score_board': score_board
    }
    return render(request, 'game/index.html', context)


def detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    return render(request, 'game/detail.html', {'game': game})


def add(request):
    if request.method == 'POST':
        form = GameForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('game_index')
    else:
        form = GameForm()

    return render(request, 'game/add.html', {'form': form})


@login_required
def organizations_list(request):
    user_organizations = request.user.organizations.all()

    return render(request, 'organization/list.html', {
        'user_organizations': user_organizations,
    })
