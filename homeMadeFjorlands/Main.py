from RobotController import Robot


if __name__ == "__main__":
    print("\n\nStarting!\n")
    robot = Robot(False)
    robot.camera.startVideoCapture(robot)
    


