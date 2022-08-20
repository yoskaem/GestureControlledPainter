# GestureControlledPainter
Recognizes hand gestures to virtually paint. 

Run the 'VirtualPainter.py' file. It will access the 'HandTrackerModule.py' file. 
You will also need to add 'opencv-python' and 'mediapipe' to the interpreter. (Use 'mediapipe-silicon' if you're on a Mac with Apple silicon chip)
The images for the overlays are saved in the 'Header' and 'Size' folder. 

There are five modes (hand gestures) available: 

1. Selection mode: This mode is active when only holding the pointer and middle finger up. 
    Select a color from the top (black is the eraser) and a brush size from the left.
    
2. Drawing mode: This mode is active when only holding the pointer up.
    Allows you to draw or erase.
    
3. Save mode: This mode is active when only holding the pointer and pinky up. 
    This will save the shapes you drew (only triangles, quadrilaterals, and lines) in a list.
    
4. Fix mode: This mode is active when only holding the pointer, middle finger, and pinky up.
    This will 'fix' the last shape in the list of saved shapes from mode 'save mode', meaning it will make the lines straight. 
    
5. Fix all mode: This mode is active when only holding the pointer, middle finger, ring finger, and pinky up. 
    This will fix all shapes in the list of saved shapes. 
    
Make sure to lower fingers before lifting others up to not accidentally enter a wrong mode. 
I recommend holding up all fingers if neccessary since it won't enter any mode like that. 
