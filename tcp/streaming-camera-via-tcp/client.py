import socket, pickle, cv2,json 


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 8081
s.connect((HOST, PORT))
cap = cv2.VideoCapture(0)
while True:
	ret,photo = cap.read()
	cv2.imshow('streaming-client',photo)
	ret,buffer = cv2.imencode(".jpg",photo,[int(cv2.IMWRITE_JPEG_QUALITY),30])
	x_as_bytes = pickle.dumps(buffer)
	s.sendto((x_as_bytes),(HOST,PORT))
	received = s.recv(1024)
	received = received.decode("utf-8")
	print(received)
	if cv2.waitKey(1)==13:
		break
cv2.destroyAllWindows()
cap.release()