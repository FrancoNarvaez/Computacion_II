import asyncio
from aiohttp import web
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO

async def process_image(content):
    try:
        image = Image.open(BytesIO(content))
        grayscale_image = image.convert('L')
        output_buffer = BytesIO()
        grayscale_image.save(output_buffer, format='JPEG')
        processed_image = output_buffer.getvalue()
        print('Processed image')
        return processed_image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

async def handle_request(request):
    if request.method == 'POST':
        content = await request.read()
        processed_image = await process_image(content)
        if processed_image is not None:
            print('Sent processed image')
            return web.Response(body=processed_image, content_type='image/jpeg')
        else:
            return web.Response(status=500)
    else:
        return web.Response(status=404)

app = web.Application()
app.router.add_route('*', '/process_image', handle_request)
web.run_app(app, host='::', port=8888)
