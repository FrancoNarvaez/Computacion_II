import asyncio
import aiohttp
from aiohttp import web
from aiohttp import ClientSession
from PIL import Image
from io import BytesIO

async def process_image(content):
    try:
        image = Image.open(BytesIO(content))
        grayscale_image = image.convert('L')
        output_buffer = BytesIO()
        grayscale_image.save(output_buffer, format='PNG')
        processed_image = output_buffer.getvalue()
        print('Processed image')
        return processed_image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

async def send_image_to_server_2(processed_image, scale_factor):
    data = aiohttp.FormData()
    data.add_field('image', processed_image, filename='image.png', content_type='image/png')
    data.add_field('scale_factor', str(scale_factor))
    async with ClientSession() as session:
        async with session.post('http://[::]:8889/resize_image', data=data) as response:
            print('Sent processed image to server 2')
            imagen_final = await response.read()
            return imagen_final

async def handle_request(request):
    if request.method == 'POST':
        data = await request.post()
        content = data['image'].file.read()
        scale_factor = float(data['scale_factor'])
        processed_image = await process_image(content)
        imagen_final = await send_image_to_server_2(processed_image, scale_factor)
        if imagen_final is not None:
            return web.Response(body=imagen_final, content_type='image/png')
        else:
            return web.Response(status=500)
    else:
        return web.Response(status=404)

app = web.Application()
app.router.add_route('*', '/process_image', handle_request)
web.run_app(app, host='::', port=8888)