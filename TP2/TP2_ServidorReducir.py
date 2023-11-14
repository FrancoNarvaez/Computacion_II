import asyncio
from aiohttp import web
from PIL import Image
from io import BytesIO

async def resize_image(content, scale_factor):
    try:
        image = Image.open(BytesIO(content))
        new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        resized_image = image.resize(new_size)
        output_buffer = BytesIO()
        resized_image.save(output_buffer, format='PNG')
        processed_image = output_buffer.getvalue()
        print('Resized image')
        return processed_image
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None

async def handle_request(request):
    if request.method == 'POST':
        data = await request.post()
        content = data['image'].file.read()
        scale_factor = float(data['scale_factor'])
        processed_image = await resize_image(content, scale_factor)
        if processed_image is not None:
            print('Sent resized image')
            return web.Response(body=processed_image, content_type='image/png')
        else:
            return web.Response(status=500)
    else:
        return web.Response(status=404)

app = web.Application()
app.router.add_route('*', '/resize_image', handle_request)
web.run_app(app, host='::', port=8889)