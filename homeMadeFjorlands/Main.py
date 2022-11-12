from RobotController import Robot

if __name__ == "__main__":

    print("\n\nStarting!\n")
    robot = Rover()
    image = robot.camera.startVideoCapture(robot)
    robot.update(image)
