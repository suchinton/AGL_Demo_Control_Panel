import can

def send_can_signal(frame):
    msg = separate_can_frame(frame)
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    #msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
    try:
        bus.send(msg)
        print("CAN signal sent successfully:")
        print("CAN ID:", hex(msg.arbitration_id))
        print("Data:", msg.data)
        if frame!="021#FFFFFFFF00000000":
            # Turn off signal
            send_can_signal("021#FFFFFFFF00000000")

    except can.CanError:
        print("Failed to send CAN signal")
    finally:
        bus.shutdown()

def separate_can_frame(frame):
    
    # split the frame into arbitration ID and data parts
    arb_id, data = frame.split("#")
    arb_id = int(arb_id, 16)
    data = bytes.fromhex(data)
    message = can.Message(arbitration_id=arb_id, data=data)
    return message


def main():
    frame = "021#FFFFFFFF10000000"
    send_can_signal(frame)

if __name__ == "__main__":
    main()
