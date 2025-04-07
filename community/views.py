from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Upvote, Notification
from .forms import CommentForm
from .models import Post
from django.contrib import messages

@login_required
def Posts(request):
    if request.method == 'POST':
        post = request.POST.get('post_description')

        Post.objects.create(
                user=request.user,
                post=post,
                num_comments=0,
                num_upvotes=0
        )
        messages.success(request, "Post added successfully!")
        other_users = User.objects.exclude(id=request.user.id)
        for user in other_users:
            Notification.objects.create(
                user=user,
                notification=f"{request.user.username} added a new post."
            )
        return redirect('community')  # Redirect after adding the skill

    return render(request, 'add_post.html', {'message': messages})




def posts_with_comments(request):
    posts = Post.objects.all().prefetch_related('comments')

    # Track upvoted posts only if the user is logged in
    upvoted_posts = set()
    if request.user.is_authenticated:
        user_upvotes = Upvote.objects.filter(user=request.user)
        upvoted_posts = {upvote.post.id for upvote in user_upvotes}  # set of post IDs user has upvoted

        # Handle comment form submissions only for authenticated users
        if request.method == 'POST' and 'comment' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            
            form = CommentForm(request.POST)
            if form.is_valid():
                # Save the comment to the post
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                post.num_comments += 1  # increment comment count on post
                post.save()
                if post.user != request.user:
                    Notification.objects.create(
                        user=post.user,
                        notification=f"{request.user.username} commented on your post."
                    )
                return redirect('community')  # Refresh the page

    context = {
        'posts': posts,
        'upvoted_posts': upvoted_posts,
        'comment_form': CommentForm() if request.user.is_authenticated else None,
    }
    return render(request, 'community.html', context)

@login_required
def toggle_upvote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    upvote, created = Upvote.objects.get_or_create(user=request.user, post=post)

    if created:
        # New upvote added
        post.num_upvotes += 1
        post.save()
        upvoted = True
        if post.user != request.user:
            Notification.objects.create(
                user=post.user,
                notification=f"{request.user.username} upvoted your post."
            )
    else:
        # Upvote exists; remove it
        upvote.delete()
        post.num_upvotes -= 1
        post.save()
        upvoted = False

    return JsonResponse({'upvoted': upvoted, 'num_upvotes': post.num_upvotes})


@login_required
def notifications(request):
    user_notifications = request.user.notifications.order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': user_notifications})

