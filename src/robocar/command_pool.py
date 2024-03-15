import queue
import threading

command_queue = queue.Queue()


def set_motor_speed(speed):
    print(f"Speed has been set to {speed}")


def steer_left(speed):
    print(f"Steering left at {speed}")


def steer_right(speed):
    print(f"Steering right at {speed}")


def cleanup():
    print("Cleaning up GPIO pins")


def command_producer():
    try:
        while True:
            command = input("Enter command: ")
            command_queue.put(command)
            if command == "q":
                break
    except KeyboardInterrupt:
        print("Exiting producer")
    finally:
        command_queue.put("q")


def command_consumer():
    try:
        while True:
            command = (
                command_queue.get()
            )  # This will block until a command is available
            if command == "f":
                set_motor_speed(50)  # Example function to set speed
            elif command == "s":
                set_motor_speed(0)  # Stop the motor
            elif command == "l":
                steer_left(20)  # Example function to steer left
            elif command == "r":
                steer_right(20)  # Example function to steer right
            elif command == "q":
                break  # Exit loop
            command_queue.task_done()
    except KeyboardInterrupt:
        print("Exiting consumer")
    finally:
        cleanup()


producer_thread = threading.Thread(target=command_producer)
consumer_thread = threading.Thread(target=command_consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()
