from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from actions.utils import create_action
from common.decorators import ajax_required
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
            create_action(request.user, "bookmarked image", new_item)
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


@ajax_required
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
                create_action(request.user, "likes", image)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Image not found"})

    return JsonResponse({"status": "error"})


@login_required
def image_list(request):
    images = Image.objects.all()
    IMAGE_PER_PAGE = 8
    paginator = Paginator(images, IMAGE_PER_PAGE)
    page = request.GET.get("page")

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(
            request,
            "images/image/list_ajax.html",
            {"section": "images", "images": images},
        )

    return render(
        request, "images/image/list.html", {"section": "images", "images": images}
    )
