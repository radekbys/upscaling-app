from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from upscaling.services.upscaling import conv_upscaling, trans_upscaling

import io


@api_view(["POST"])
def conv_upscaling_view(request):
    if "image" not in request.FILES:
        return JsonResponse({"error": "No image uploaded"}, status=400)

    image = request.FILES["image"]
    upscaled = conv_upscaling(image=image)

    buffer = io.BytesIO()
    upscaled.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")


@api_view(["POST"])
def trans_upscaling_view(request):
    if "image" not in request.FILES:
        return JsonResponse({"error": "No image uploaded"}, status=400)
    image = request.FILES["image"]
    upscaled = trans_upscaling(image=image)

    buffer = io.BytesIO()
    upscaled.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")
