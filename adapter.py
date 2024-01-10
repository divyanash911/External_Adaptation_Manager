import socket
import time


SWIM_PORT = 4242
RT_THRESHOLD = 0.75
DIMMER_STEP = 0.1


def Communication_Instance(msg):

	client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

	server_address = ('localhost',SWIM_PORT)
	client_socket.connect(server_address)

	client_socket.send(msg.encode('utf-8'))
	response = client_socket.recv(1024)

	client_socket.close()

	return response

def Get_Total_Utils():
	count = int(Communication_Instance("get_active_servers"))
	
	total = 0
	print("Active servers : " , count)
	if count < 1:
		return
	
	for i in range(1,count+1):
		string = "get_utilization server" + str(i)
		value = Communication_Instance(string)
		total = total + float(value)

	return total

def balance_load():
	
	if float(Communication_Instance("get_active_servers")) < float(Communication_Instance("get_max_servers")):
		Communication_Instance("add_server")
		print("Adding server! Total servers currently in system = " , float(Communication_Instance("get_active_servers")))
	else:
		value = max(0,float(Communication_Instance("get_dimmer")) - DIMMER_STEP)
		string = "set_dimmer " + str(value)
		print(Communication_Instance(string))
		print("Dimmer value set to " , value)


def load_checker():
	
	while 1:
		dimmer = float(Communication_Instance("get_dimmer"))
		if "error" in str(Communication_Instance("get_active_servers"),'UTF-8'):
			break

		response_time = float(Communication_Instance("get_basic_rt"))
		opt_resp_time = float(Communication_Instance("get_opt_rt"))
		basic_throughput = float(Communication_Instance("get_basic_throughput"))
		opt_throughput = float(Communication_Instance("get_opt_throughput"))

		response_time = (basic_throughput*response_time + opt_throughput*opt_resp_time)/(basic_throughput + opt_throughput)
		
		print("####Response time : " , response_time , "####")
		if response_time > RT_THRESHOLD:
			balance_load()
		
		else :
			spare_util = float(Communication_Instance("get_active_servers")) - Get_Total_Utils()
			
			if spare_util > 1:
				current_dimmer = float(Communication_Instance("get_dimmer"))
				if current_dimmer < 1 :
					dimmer = min(1,current_dimmer+DIMMER_STEP)
					string = "set_dimmer "+str(dimmer)
					Communication_Instance(string)
					print("Dimmer value set to " , dimmer)
				else : 
					Communication_Instance("remove_server")
					print("Removing server! Total servers currently in system = " , float(Communication_Instance("get_servers")))

		time.sleep(60)

load_checker()
