import instax
import time
import traceback

while True:
	try:
		myInstax = instax.SP2(port=8080, pinCode=4782, timeout=10)
		info = myInstax.getPrinterInformation()
		print(info)
		time.sleep(1)
	except:
		print("Fail")
		print(traceback.format_exc())
		time.sleep(1)
		pass