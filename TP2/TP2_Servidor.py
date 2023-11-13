import asyncio
from aiohttp import web
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO

async def process_image(content):
    image = Image.open(BytesIO(content))
    grayscale_image = image.convert('L')

    output_buffer = BytesIO()
    grayscale_image.save(output_buffer, format='JPEG')
    processed_image = output_buffer.getvalue()
    print('Processed image')
    return processed_image

async def handle_request(request):
    if request.method == 'POST':
        content = await request.read()

        # Process the image
        processed_image = await process_image(content)

        # Send the processed image to the client
        return web.Response(body=processed_image, content_type='image/jpeg')
        print('Sent processed image')
    else:
        return web.Response(status=404)

app = web.Application()
app.router.add_route('*', '/process_image', handle_request)

# Iniciar el servidor en todas las interfaces de red (IPv4 e IPv6)
web.run_app(app, host='::', port=8888)