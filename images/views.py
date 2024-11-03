from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from images.forms import ImageCreateForm
from images.models import Image


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)

            new_item.user = request.user
            new_item.save()
            messages.success(request, "Image Uploaded successfully")

            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    return render(
        request, "images/image/create.html", {"section": "images", "form": form}
    )


def image_details(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request, "images/image/detail.html", {"section": "images", "image": image}
    )


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)

            if action == "like":
                image.user_like.add(request.user)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Image not found"})

    return JsonResponse({"status": "error"})