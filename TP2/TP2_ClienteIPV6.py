import aiohttp
import asyncio

async def send_image_to_server(image_path):
    with open(image_path, 'rb') as file:
        image_data = file.read()

    async with aiohttp.ClientSession() as session:
        async with session.post('http://[::]:8888/process_image', data=image_data) as response:
            response_data = await response.read()

            # Guardar la imagen recibida en un archivo
            with open('received_image.jpg', 'wb') as out_file:
                out_file.write(response_data)

            print('Received and saved image')

async def main():
    await send_image_to_server('/home/franconarvaez/Escritorio/Computacion_II/TP2/linuxImagen.jpeg')

asyncio.run(main())