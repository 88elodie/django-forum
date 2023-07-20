from posts.models import Board, Post
from django.shortcuts import render

def home(request):
    boards = Board.objects.all()
    for board in boards:
        post_count = Post.objects.filter(board_id=board.id).count()
        board.post_count = post_count

    return render(request, 'home.html', context={"boards":boards})

