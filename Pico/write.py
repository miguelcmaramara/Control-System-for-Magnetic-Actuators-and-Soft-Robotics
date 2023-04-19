from machine import UART


def writeSteps(ex1, ex2, ey, er, uart, state, method, rate):
    if state == True:
        message = str(ex1.get_steps()) + ',' + str(ex2.get_steps()) + ',' + str(ey.get_steps()) + ',' +str(er.get_steps()) + '\n'
        message.encode()
        uart.write(message)
    
    return 