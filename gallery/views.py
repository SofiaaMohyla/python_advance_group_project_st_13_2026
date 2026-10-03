from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .forms import GalleryForm
from .models import Gallery


def gallery(request):
    materials = Gallery.objects.all().order_by('-created_at')
    paginator = Paginator(materials, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'gallery/gallery.html', {
        'materials': page_obj
    })


@login_required
def upload_gallery(request):
    if not request.user.can_upload:
        return redirect('gallery')

    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)

        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.uploaded_by = request.user
            gallery.save()

            return redirect('gallery')
    else:
        form = GalleryForm()

    return render(request, 'gallery/upload.html', {
        'form': form
    })


@login_required
def delete_gallery(request, pk):
    material = get_object_or_404(Gallery, pk=pk)

    if material.uploaded_by == request.user or request.user.role in ['moderator', 'admin']:
        material.delete()

    return redirect('gallery')
@login_required
def manage_uploads(request):
    if request.user.role != 'admin':
        return redirect('gallery')

    User = get_user_model()

    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.POST.get('user_id'))
        user.can_upload = not user.can_upload
        user.save()

    users = User.objects.all()

    return render(request, 'gallery/manage_uploads.html', {
        'users': users
    })