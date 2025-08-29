from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django_app.upscalers.conv_upscaling import conv_upscaling

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

    # return JsonResponse(
    #     {
    #         "message": "api works",
    #         "which_endpoint": "conv",
    #         "filename": image.name,
    #         "size": image.size,
    #         "content_type": image.content_type,
    #     }
    # )


@api_view(["POST"])
def trans_upscaling_view(request):
    if "image" not in request.FILES:
        return JsonResponse({"error": "No image uploaded"}, status=400)
    return JsonResponse({"message": "api works", "which_endpoint": "transformer"})
