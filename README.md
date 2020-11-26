# Client Handover Document 
## Sign detection using neural network 
**Team CP32B**

## Project Description

We are moving closer to autonomous cars and drones every day and finding new ways of using AI in the real world in other applications (fighting pandemics, object classification). 

In this project, we will implement both a real word and simulated world traffic sign detection algorithms using a combination of computer vision (openCV) Neural Network (TensorFlow). The simulated data will be collect using Donkey Car simulator, and there is another project component focusing on simulator improvements. We looked at different algorithms to come up with robust and efficient solution.

---
## Documents

- [Proposal Document](https://github.com/wallarug/capstone2020/blob/master/proposals/CP32%20-%20Project%20Proposal.pdf)
- [Requirements Document](https://github.com/wallarug/capstone2020/blob/master/requirements/CP32%20-%20Scope%20and%20Requirements%20Document%20September%202020.pdf)
- [Updated Requirements Document](https://github.com/wallarug/capstone2020/blob/master/requirements/CP31%20and%20CP32%20-%20Further%20Scope%20Information%20for%20Simulator.pdf)

---
## Team Memeber Information

| First Name | Name on Discord  | Email Address              | Main Role                                          |
| ---------- | ---------------- | -------------------------- | -------------------------------------------------- |
| Yuanda     | CP32B-Yuanda     | ydon4228@uni.sydney.edu.au | Tensorflow + OpenCV (testing), RMracerlib          |
| Yiran      | CP32B-Yiran      | yjin5856@uni.sydney.edu.au | Tensorflow + OpenCV (model)                        |
| Mouyi      | CP32B-MOUYI XU   | moxu7046@uni.sydney.edu.au | Unity (tracks)                                     |
| Robert     | CP32B-Robert Jia | sjia0385@uni.sydney.edu.au | Blender (create car model)                         |
| Hao        | CP32B-Hao        | hlan3540@uni.sydney.edu.au | Tensorflow                                         |
| Nicole     | CP32B-Nicole     | zhua4138@uni.sydney.edu.au | Blender (create assets such as traffic signs etc.) |

## Video Summaries

### Weekly Updates
| Week | Yuanda                                                       | Yiran                                   | Mouyi                                   | Robert                                                       | Hao                                     | Nicole                                  |
| ---- | ------------------------------------------------------------ | --------------------------------------- | --------------------------------------- | ------------------------------------------------------------ | --------------------------------------- | --------------------------------------- |
| 4    | [YouTube](https://youtu.be/d9mRQXM1_dc)                      | [YouTube](https://youtu.be/NJyp6R7ZGR0) | [YouTube](https://youtu.be/_2eW4pzh7tE) | [YouTube](https://youtu.be/NiPeBPrbKXM)                      | [YouTube](https://youtu.be/7U-fWr5Sv_E) | [YouTube](https://youtu.be/dX4lj7Y1JFY) |
| 5    | [YouTube](https://www.youtube.com/watch?v=-Ea1S9x55oQ&feature=youtu.be) | [YouTube](https://youtu.be/Pdbp4nOL8Lk) | [YouTube](https://youtu.be/2FwnLP4FiB0) | [YouTube](https://youtu.be/d3iy-GJf6XI)                      | [YouTube](https://youtu.be/JvlqVd-pQZo) | [YouTube](https://youtu.be/KkBae-5aGnw) |
| 6    | [YouTube](https://www.youtube.com/watch?v=hWSs6zBgu_s&feature=youtu.be) | [YouTube](https://youtu.be/6CO-E7Vt03I) | [YouTube](https://youtu.be/adVbw1as3VE) | [YouTube](https://youtu.be/-kTnFZG_Ac4)                      | [YouTube](https://youtu.be/--aVURGKhNk) | [YouTube](https://youtu.be/aACL0KiHaO8) |
| 7    |                                                              | [YouTube](https://youtu.be/3xD5ec7F6L8) | [YouTube](https://youtu.be/S7HMbG-Ljqc) | [YouTube](https://youtu.be/fGYtrB7iZmA)                      | [YouTube](https://youtu.be/lX3zUaQVL3Q) | [YouTube](https://youtu.be/AEior8RGtFQ) |
| 8    |                                                              | [YouTube](https://youtu.be/lp8B9a6NXHw) | [YouTube](https://youtu.be/S7HMbG-Ljqc) | [YouTube](https://youtu.be/UZG1vpD1AS0)                      | [YouTube](https://youtu.be/x0gUSXXUKaI) | [YouTube](https://youtu.be/6HWmnvg1lpU) |
| 9    |                                                              | [YouTube](https://youtu.be/nntQoA_ZGRM) | [YouTube](https://youtu.be/xOlWfW1SABQ) | [YouTube](https://www.youtube.com/watch?v=tltSKE9agMs&feature=youtu.be) | [YouTube](https://youtu.be/BjYLYZGwsJE) | [YouTube](https://youtu.be/-AnldWgdCXE) |
| 10   |                                                              | [YouTube](https://youtu.be/ZBgl6bLZNFs) | [YouTube](https://youtu.be/z_Aa4tvAlOI) | [YouTube](https://www.youtube.com/watch?v=b1Enooe4wRc&feature=youtu.be) | [YouTube](https://youtu.be/M33l6vhlL0E) | [YouTube](https://youtu.be/FWF6cEYGq8Y) |
| 11   |                                                              | [YouTube](https://youtu.be/AdHaU4O7G_g) | [YouTube](https://youtu.be/AINMHtjeVyo) | [YouTube](https://www.youtube.com/watch?v=iSuoB33_i0A&feature=youtu.be) | [YouTube](https://youtu.be/NDRO-ccFWfo) | [YouTube](https://youtu.be/KdtCmdEQZ78) |
| 12   |                                                              | [YouTube](https://youtu.be/zU0vtKoXRBM) | [YouTube](https://youtu.be/eqNrKk2x5V4) | [YouTube](https://www.youtube.com/watch?v=J37EGAt-KQs&feature=youtu.be) | [YouTube](https://youtu.be/AWeeRJO3CE0) | [YouTube]()                             |
| 13   |                                                              |                                         | [YouTube](https://youtu.be/rKrkwmnWJ7c) | [YouTube](https://www.youtube.com/watch?v=Qvmi7Z04hxA&feature=youtu.be) |                                         |                                         |

### Major Milestones

| Milestone               | Video                                                        |
| ----------------------- | ------------------------------------------------------------ |
| First client deployment | [YouTube](https://www.youtube.com/watch?v=_W_JX03uFBE&list=PLfwiy0wVlGXwtHwRymVrPehrioXkUKPEg&index=6&t=2008s) |
| Final client deployment | [YouTube](https://www.youtube.com/watch?v=6H6geVCDLH8), starting from 1:05:40 |
| Project showreel        | [YouTube](https://www.youtube.com/watch?v=VxKC9a5ixNI&feature=youtu.be) |




---
## Repository content and documentation

1. [Simulator](https://github.com/Yuanda-Dong/Client-Final-Deployment/tree/main/Simulator)
2. [Source code of Sign Detection Model](https://github.com/Yuanda-Dong/Client-Final-Deployment/tree/main/SourceCode)
3. [RMracerlib](https://github.com/Yuanda-Dong/Client-Final-Deployment/tree/main/rmracerlib)


## Goal & Deliverables

`TODO @wallarug:  insert table of deliverables for each project`

## Testing Results

`TODO @wallarug: insert table of testing for each project with link to data.`

