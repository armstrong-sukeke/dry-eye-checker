sudo docker pull nvcr.io/nvidia/l4t-ml:r32.5.0-py3
# Replace "nvidia" in the volume option with your username
sudo docker run --runtime nvidia -it --rm --network host -e DISPLAY=$DISPLAY --volume /home/nvidia/dry-eye-checker/shared_data:/shared_data --device /dev/video0 nvcr.io/nvidia/l4t-ml:r32.5.0-py3