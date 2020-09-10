vid = videoinput('linuxvideo',1);
aviObject = VideoWriter('myVideo.avi');   % Create a new AVI file
set(vid, 'FramesPerTrigger', 30);
set(vid, 'TimerPeriod', 0.03333);
set(vid, 'ReturnedColorspace', 'rgb');
vid.FrameGrabInterval = 1;  % distance between captured frames(1 captures every frame)
source = getselectedsource(vid);
frameRates = set(source, 'FrameRate');
fps = frameRates{1};
source.FrameRate = fps;

%aviObject.FrameRate = fps;
aviObject.FrameRate = str2double(fps);
open(aviObject);
I=getsnapshot(vid);
for iFrame = 1:100                    % Capture 100 frames
  I=getsnapshot(vid);
  F = im2frame(I);                    % Convert I to a movie frame
  writeVideo(aviObject,F);  % Add the frame to the AVI file
end
close(aviObject);         % Close the AVI file
stop(vid);

flushdata(vid);
