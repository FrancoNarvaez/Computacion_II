# Cliente
import aiohttp
import asyncio
import argparse
from datetime import datetime

async def send_image_to_server(image_path):
    try:
        with open(image_path, 'rb') as file:
            image_data = file.read()
        async with aiohttp.ClientSession() as session:
            async with session.post('http://[::]:8888/process_image', data=image_data) as response:
                response_data = await response.read()
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                with open(f'received_image_{timestamp}.jpg', 'wb') as out_file:
                    out_file.write(response_data)
                print('Received and saved image')
    except Exception as e:
        print(f"Error sending image to server: {e}")

async def main(image_path):
    await send_image_to_server(image_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send an image to the server.', add_help=False)
    parser.add_argument('-i', '--image_path', type=str, required=True, help='The path to the image to send.')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, 
                        help='Show this help message and exit')
    args = parser.parse_args()
    asyncio.run(main(args.image_path))