SERVER_IP = '::1'  # Escucha en todas las interfaces de red
SERVER_PORT = 8080

CLIENTS = [
    {
        'ip': '::1',  # IPv6
        'port': 8080
    },
    {
        'ip': '127.0.0.1',  # o '127.0.0.1' IPv4
        'port': 8080
    },
]
"""{
    'ip': 'localhost',  # o '127.0.0.1' IPv4
    'port': 8080
},
{
    'ip': '::1',  # IPv6
   'port': 8080
},
{
    'ip': 'localhost',  # o '127.0.0.1' IPv4
    'port': 8080
},
{
    'ip': 'localhost',  # o '127.0.0.1' IPv4
    'port': 8080
},"""
