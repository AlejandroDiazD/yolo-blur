docker run -it \
  --name yolo-blurr \
  --network host \
  -v "$(pwd)":/home/yolo-blurr \
  ultralytics/ultralytics:latest-cpu \
  /bin/bash -c "python3 -m pip install -r /home/yolo-blurr/requirements.txt && cd /home/yolo-blurr/code && bash"
