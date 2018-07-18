# solitons-video-measurement
University Lab Tool. Measures the water level from each frame of lab footage.

The bottom picture is the current frame being analysed. On each one of them, the 8cm graduation needs to be found because the camera tried to stabilise the image causing it to be wobbly- an unfortunated discovery made when all the footage was recorded! One can see the calibration zone on the right where the 8cm graduation is detected. The other graduations follow on as the spacing between each millimeter remains the same. The water level is detected with a matplotlib contouring tool and is then measured as waves pass in front of the camera.

The top graph plots the water level measured on each frame. The accuracy is remarkable. This tool gathered more than 30,000 data points which would have been otherwise collected by hand. The abundance of data allowed detailed analysis of the phenomenon.

![gif screenshot](prgm_rec.gif)
