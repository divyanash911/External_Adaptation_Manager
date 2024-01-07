import socket
SWIM_PORT = 4242
RT_THRESHOLD = 10
DIMMER_STEP = 0.1
def Communication_Instance(msg):

	client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

	server_address = ('localhost',SWIM_PORT)
	client_socket.connect(server_address)

	client_socket.send(msg.encode('utf-8'))
	response = client_socket.recv(1024)

	client_socket.close()

	return response

def Get_Probes():

	print(float(Communication_Instance("get_active_servers")))
	print(float(Communication_Instance("get_arrival_rate")))
	print(float(Communication_Instance("get_basic_rt")))
	print(float(Communication_Instance("get_basic_throughput")))
	print(float(Communication_Instance("get_dimmer")))
	print(float(Communication_Instance("get_max_servers")))
	print(float(Communication_Instance("get_opt_rt")))
	print(float(Communication_Instance("get_opt_throughput")))
	print(float(Communication_Instance("get_servers")))


def balance_load():
	
	if float(Communication_Instance("get_active_servers")) < float(Communication_Instance("get_max_servers")):
		print(Communication_Instance("add_server")))
	else:
		value = max(0,float(Communication_Instance("get_dimmer")) - DIMMER_STEP)
		print(Communication_Instance(f"set_dimmer {value}"))


def load_checker():
	
	while 1:
		
		if "error" in Communication_Instance("get_active_servers"):
				
			break
		else:
			pass

		
		response_time = float(Communication_Instance("get_basic_rt")
		
		if response_time > RT_THRESHOLD :
			balance_load()
		
		else :
			pass
					

