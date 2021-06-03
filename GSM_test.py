from BrainWheel.embedded_system.GSM import *


# x = GSM.send_message(GSM_phone_num, GSM_message)
x = GSM.call(GSM_phone_num)
print(x)