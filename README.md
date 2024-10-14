# docker pull stereolabs/kalibr


`
docker pull stereolabs/kalibr
`

`
docker run -it -e "DISPLAY" -e "QT_X11_NO_MITSHM=1" -v "/tmp/.X11-unix:/tmp/.X11-unix:rw" -v "./:/data" stereolabs/kalibr

`


### run

### create bag
`
kalibr_bagcreater --folder data/ --output-bag sequence.bag
`
check topic

`
rosbag info sequence.bag

`

`
kalibr_calibrate_cameras --bag sequence.bag --target aprilgrid.yaml --models 'pinhole-radtan' --topics /data/apriltags/

`
`
kalibr_calibrate_cameras 
--bag sequence.bag 
--target aprilgrid.yaml 
--models 'pinhole-radtan' 
--topics /cam2/image_raw 
--approx-sync 0.005
`# camera_calibration
