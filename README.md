# rh4-exe21b
Duckietown 2020 RH4 exe 21b

Instructions to reproduce results

### 1. Clone this repository and go to its directory
```bash
git clone https://github.com/lineojcd/rh4-exe21b.git
cd rh4-exe21b
```
### 2. Build docker image in laptop (amd64 machine)
```bash
dts devel build -f --arch amd64
```

### 3. Make sure docker image from rh4-exe21a is running. Afterwards, run rh4-exe21b docker image with the following options.
```bash
docker run -it --rm -e ROS_MASTER_URI=http://[MY_ROBOT_IP]:11311/ -e ROS_IP=http://[MY_LAPTOP_IP]:11311/ -v [PATH_ON_YOUR_LAPTOP]:[PATH_TO_BAG_FOLDER_FROM_CONTAINER] --net host duckietown/rh4-exe21b:latest-amd64
```
Image stream with color detector is published.


A sample debug image for the yellow color detector is shown here:
![testimgdector](https://github.com/lineojcd/rh4-exe21b/testimgdector.png)
