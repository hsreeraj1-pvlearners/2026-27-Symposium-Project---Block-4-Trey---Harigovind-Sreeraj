# 2026-27 Symposium Project : Block-4 Trey - Harigovind Sreeraj
All of the program files for my freshman year engineering symposium project.

Draft 1:
This draft contains the code which has random mapping. Basic movement is established, but there is not much of a deliberate mapping system. The robot will turn a random amount, move until it reaches a boundary. It tracks how much it has moved (through sine and cosine functions and the data from wheel rotation and gyro sensors) and determines where the boundary is from the ultrasonic sensor. It makes a coordinate point where the boundary is, and it will then repeat the process by turning a random amount and cycling through. It will continue this until someone breaks the code since the robot will not know when to stop.

Draft 2:
In this draft, we take the previous draft and make improve it by not having the robot rebound after just one point. Once it detects an object, it continues to cycle around the entire surface because if you follow the surface of a 3-dimensional object, you are guaranteed to eventually return to where you started. This way, we can map out full objects or connected objects instead of having a cloud of random data that would only resemble the obstacles after an unpredictable amount of time. With this method, we know that we'll map objects all at once, but since we didn't change random exploration, we still wouldn't know when the robot has fully explored a room unless it is checked manually. It also isn't predictable with how long it will take to complete mapping out a room.

Test EV3 File:
This file is not a contribution to the overall project and acts more as a verification method for the connection between the EV3 and other device (such as a laptop). This also makes sure you method of transferring files works, and since it audibly speaks a message, it is very clear.
