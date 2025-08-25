from django.http import JsonResponse
from rest_framework.decorators import api_view
from django_app.upscalers.conv_upscaling import conv_upscaling


@api_view(["POST"])
def conv_upscaling_view(request):
    if "image" not in request.FILES:
        return JsonResponse({"error": "No image uploaded"}, status=400)

    image = request.FILES["image"]
    conv_upscaling(image=image)

    return JsonResponse(
        {
            "message": "api works",
            "which_endpoint": "conv",
            "filename": image.name,
            "size": image.size,
            "content_type": image.content_type,
        }
    )


@api_view(["POST"])
def trans_upscaling_view(request):
    if "image" not in request.FILES:
        return JsonResponse({"error": "No image uploaded"}, status=400)
    return JsonResponse({"message": "api works", "which_endpoint": "transformer"})
