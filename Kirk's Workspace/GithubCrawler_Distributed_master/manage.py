# coding=utf-8
# author:Star
from DF.core.Server import Server
from DF.core.Client import Client
import sys
from DF.app.configuration import configuration

# get cmd operation
poten_opera = ['-h/-help', '-v/-version', 'run-main-server', 'run-slave-server']
operation = sys.argv[1]

if operation == '-h' or operation == '-help':
    print('Here are operations you can have:')
    for op in poten_opera:
        print(op)
elif operation == '-v' or operation == '-version':
    print(configuration.VERSION)
elif operation == 'run-slave-server':
    print('run slave server...')
    ip_address = input("Please enter main server's ip address: ")
    main_port = input("Please enter main server's port: ")
    try:
        main_port = int(main_port)
    except:
        print("Please enter a correct port number!")
        exit()
    my_port = input("Please enter an available port on your computer: ")
    try:
        my_port = int(my_port)
    except:
        print("Please enter a correct port number!")
        exit()
    client = Client(ip_address, main_port)
    client.send_message({"test":"hello world"})
    server = Server(ip_address="localhost", port=my_port)
    server.start_listen()
elif operation == 'run-main-server':
    print('run main server...')
    my_port = input("Please enter an available port on your computer: ")
    try:
        my_port = int(my_port)
    except:
        print("Please enter a correct port number!")
        exit()
    server = Server(ip_address="localhost", port=my_port)
    server.start_listen()
