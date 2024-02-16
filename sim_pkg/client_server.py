import socket
import select
import json 
import time
import errno
import queue
import numpy as np

class Bot_Server():
    def __init__(self, hostname, port, num_robots):
        '''
        Server used in the simulator
        All robots send data to the server, which get processed in the simulator
        '''
        self.hostname, self.port = hostname, port
        self.num_robots = num_robots
        self.message_queues = {} # Dictionary to store messages to send to each socket
        self.num_connected = 0
        self.fresh_pose = np.full(num_robots, False)
        self.fresh_messages = np.full(num_robots, False)
    
    def start(self):
        '''
        Create a nonblocking server socket and begin listening for incoming connections
        '''
        # print("BOT SERVER: Started") # TODO: Remove
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Open socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reuse of addresses (prevents Address Already Bound errors)
        self.server_socket.setblocking(0) # Make socket non-blocking -- instead of waiting for each operation to complete one by one, the program can check the status of multiple sockets simultaneously
        try:
            self.server_socket.bind((self.hostname, self.port)) 
        except socket.error as e:
            print("Bot Server failed to bind: ", e)
        
        self.server_socket.listen(self.num_robots) # Allow up to num_robots client connections

        # List of sockets to monitor for reading (receiving data) and writing (sending data)
        self.read_list = [self.server_socket]
        self.write_list = []

    def recv(self, swarm):
        '''
        Receive data (requests) from readable client sockets
        For certain received requests, sends responses back to the client as necessary
        '''
        # print("BOT SERVER: Receiving...") # TODO: Remove
        # Use `select` to identify which sockets are ready for I/O
        # This operation is blocking -- if no sockets are ready, it will wait until one is -- provide a small timeout to give the server time to accept any incoming client connections
        # Note: The timeout actually should not have an effect on performance until the server is running after the clients are done, since sockets will not be ready for I/O at this point
        readable, writable, _ = select.select(self.read_list, self.write_list, [], 0.2) 

        received_data = []

        # Handle receiving from clients
        for s in readable:
            if s is self.server_socket:
                # The server socket is ready to accept a client connection.
                client_socket, _ = s.accept()
                client_socket.setblocking(0)

                self.read_list.append(client_socket)
                self.message_queues[client_socket] = queue.Queue()

                # print("BOT SERVER: Client connected") # TODO: Remove

                self.num_connected += 1 

            else:
                # A client (whose connection has already been established) has sent data
                message = s.recv(1024)

                if message: 
                    # The message was not None -- send a response back to the client
                        message = message.decode("utf-8")
                        message = json.loads(message)

                        received_data.append(message)

                        client_id = message["id"]
                        client_function = message["function"]

                        if client_function == 3:
                            # get_clock
                            response = {
                                "response": swarm[client_id].clock 
                            }
                        elif client_function == 4:
                            if self.fresh_pose[client_id]:
                                response = {
                                    "response": swarm[client_id].posn
                                }
                                self.fresh_pose[client_id] = False
                            else:
                                response = {
                                    "response": False
                                }
                        elif client_function == 6:
                            if self.fresh_messages[client_id]:
                                response = {
                                    "response": swarm[client_id].message_buffer
                                }
                                self.fresh_messages[client_id] = False
                                swarm[client_id].message_buffer = [] #clear the message buffer 
                            else:
                                response = {
                                    "response": []
                                }
                        else:
                            response = {
                                "response": 1
                            }

                        response = json.dumps(response)
                        response = response.encode("utf-8")
                        self.message_queues[s].put(response) # Add response to queue of messages to be sent to client s

                        if s not in self.write_list:
                            self.write_list.append(s) # Add output channel for response
    
                # else:
                #     # No more data from the client -- close the connection
                #     print("SOCKET REMOVED!!")
                #     # self.num_connected -= 1 
                #     self.read_list.remove(s)
                #     if s in self.write_list:
                #         self.write_list.remove(s)
                #     del self.message_queues[s]
                #     s.close()

        # Handle sending to clients
        for s in writable:
            try:
                # Get next message to send to the socket (nonblocking)
                next_msg = self.message_queues[s].get_nowait()
            except queue.Empty:
                # No messages are left, so the socket is no longer writable
                self.write_list.remove(s)
            else:
                # If message was available (queue was non-empty), send message
                s.send(next_msg)
        
        # # Handle exceptions
        # for s in exceptional:
        #     print("EXCEPTIONAL LIST")
        #     self.read_list.remove(s)
        #     if s in self.write_list:
        #         self.write_list.remove(s)
        #     del self.message_queues[s]
        #     s.close()

        return received_data
    
    def stop(self):
        '''
        Close the server socket and any connected client sockets
        '''
        # print("BOT SERVER Stopped...")
        # Close the clients connected to the server before closing the server socket
        # This should help with resource cleanup, otherwise the clients may not be closed explicitly
        for s in self.read_list:
            s.close()
        self.server_socket.close()
    
class Bot_Client():
    def __init__(self, hostname, port, buffer_size, rtf):
        '''
        Client used in Coachbot API
        All robots send data through the client to the simulator server 
        '''
        self.hostname, self.port = hostname, port
        self.buffer_size = buffer_size
        self.rtf = rtf
    
    def start(self):
        '''
        Create a client socket and try to connect to the socket at the given server address
        '''
        # print("BOT CLIENT: Started.") # TODO: Remove
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.client_socket.connect((self.hostname, self.port))
        except socket.error as e:
            if e.errno == errno.EINPROGRESS:
                # `[Erno 36] Operation now in progress` occurs when a nonblocking socket operation (e.g. connect) is re-attempted before a previous attempt is finished
                time.sleep(0.05) # Allow for a small delay before retrying
            else:
                print("BOT CLIENT socket failed to connect: ", e) # TODO: Remove, otherwise clients error after server disconnects
    
    def send(self, data):
        '''
        Process data and send to the server
        '''
        # NOTE: the client is actually blocking -- it will wait for a response from the server before doing things
        # print("BOT CLIENT: sending")
        raw_data = data
        data = json.dumps(data)
        data = data.encode("utf-8")

        # Send data
        self.client_socket.sendall(data)

        # Receive response from simulator
        response = self.client_socket.recv(self.buffer_size)

        # Need to keep the socket open for a tiny bit
        #want it to be open for 20ms at rtf = 1 
        # time.sleep(0.02/self.rtf)
        time.sleep(0.001/self.rtf)

        if not response:
            time.sleep(0.2) # Need to wait a longer period to prevent "OSError: [Errno 9] Bad file descriptor" at the end of the simulation (i.e. socket closed after reading only part of the data)
            # print("CLIENT STOPPED!!!") # TODO: Remove
            self.client_socket.close()
            self.stop()
        else:
            response = response.decode("utf-8")
            response = json.loads(response)

        #actually do the sleeping here (if robot.delay)
        if raw_data["function"] in [8, 9]:
            #we have already slept 0.001 s of REAL time. Here we sleep off the rest IFF user asked for something > 0.001 s real time
            #Robot delay accepts a time value in ms!!
            delay_time = raw_data["params"]/1000
            if delay_time > 0.001:
                delay_time_remaining = (delay_time - 0.001)
                time.sleep(delay_time_remaining/self.rtf)

        if response:
            return response
        else:
            # Sometimes response = b'', in which case, we want to return something the Coachbot API can handle
            return {'response': False}
        
    def stop(self):
        '''
        Close the client socket
        '''
        # print("BOT CLIENT Stopped") #TODO: Remove
        self.client_socket.close()

    def manage_thread(self, data):
        '''
        Manage threading and thread ordering here. Executed as part of the "start new loop" api call.
        NOTE: on the real robots, this "start new loop" is just a delay function.
        '''

        self.send(data)
