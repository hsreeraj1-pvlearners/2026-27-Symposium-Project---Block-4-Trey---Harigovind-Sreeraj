# 2026-27 Symposium Project : Block-4 Trey - Harigovind Sreeraj
All of the program files for my freshman year engineering symposium project.

Draft 1:
This draft contains the code which has random mapping. Basic movement is established, but there is not much of a deliberate mapping system. The robot will turn a random amount, move until it reaches a boundary. It tracks how much it has moved (through sine and cosine functions and the data from wheel rotation and gyro sensors) and determines where the boundary is from the ultrasonic sensor. It makes a coordinate point where the boundary is, and it will then repeat the process by turning a random amount and cycling through. It will continue this until someone breaks the code since the robot will not know when to stop.
