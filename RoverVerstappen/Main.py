from Rover import RoverHandler

if __name__ == "__main__":
    print("\n\nStarting!\n")
    robot = RoverHandler()
    robot.mainThread


    # print("Final L: ", robot.LWheel.encoder.getVelocity(sampleSize=50))
    # print("Final R: ", robot.RWheel.encoder.getVelocity(sampleSize=50))