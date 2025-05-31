from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Post, Upvote, Notification, Comment,Report
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


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
        return redirect('community') 

    return render(request, 'add_post.html', {'message': messages})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        if post.user == request.user or request.user.is_staff:
            
            Comment.objects.filter(post=post).delete()
            Upvote.objects.filter(post=post).delete()
            post.delete()
            messages.success(request, "Post deleted successfully.")
            return redirect('public_profile', username=post.user.username)
        else:
            messages.error(request, "You do not have permission to delete this post.")
            return redirect('community')

    return render(request, 'delete_post.html', {'post': post})


def posts_with_comments(request):
  
    posts = Post.objects.all().order_by('-id').prefetch_related('comments')

    upvoted_posts = set()
    if request.user.is_authenticated:
        user_upvotes = Upvote.objects.filter(user=request.user)
        upvoted_posts = {upvote.post.id for upvote in user_upvotes}

        
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
                post.num_comments += 1  
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
        
        post.num_upvotes += 1
        post.save()
        upvoted = True
        if post.user != request.user:
            Notification.objects.create(
                user=post.user,
                notification=f"{request.user.username} upvoted your post."
            )
    else:
        
        upvote.delete()
        post.num_upvotes -= 1
        post.save()
        upvoted = False

    return JsonResponse({'upvoted': upvoted, 'num_upvotes': post.num_upvotes})


@login_required
def notifications(request):
    user_notifications = request.user.notifications.order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': user_notifications})

@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        reason = request.POST.get('report_reason')
        Report.objects.create(user=request.user, post=post, reason=reason)
        messages.success(request, "Post reported successfully.")
        return redirect('community')

    return render(request, 'report_post.html', {'post': post})

@user_passes_test(lambda u: u.is_staff)  
def view_reports(request):
    reports = Report.objects.all().order_by('-timestamp')
    return render(request, 'view_reports.html', {'reports': reports})

@user_passes_test(lambda u: u.is_staff)
def delete_reported_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
       
        Comment.objects.filter(post=post).delete()
        Upvote.objects.filter(post=post).delete()
        post.delete()
        messages.success(request, "Reported post deleted successfully.")
        return redirect('view_reports') 

    return redirect('view_reports')