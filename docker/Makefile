target: build

build:
	docker build . -t ros_noetic:base

run:
	docker run -it --rm --name rosbag_img_extract -v "$(ROSBAG_DIR):/data" ros_noetic:base
