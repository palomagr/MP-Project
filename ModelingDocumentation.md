The “displacement” command on Rhino isn’t available on Mac, so I looked into other methods. 
I tried using Grasshopper, looking for other commands/methods people have used with Rhino, and looking into online photogrammetry programs, but those were either unsuccessful or required too much work/time. I ended up finding a tutorial on the “heightfield” command, which I used with a black and white outline of the wall that I traced on Photoshop. 
Here's my final process:
1. Get an image of the wall, either from the dropbox or Google Earth.
2. Go into Photoshop or another photo-editing app, make the image a background layer, then trace over it on another layer.
3. Hide the background layer and export the image. In Rhino, use the Heightfield command with that image. If needed, scale the wall to the correct size using the Scale1D command.
4. Erase the former flat wall that was there before. (If it's part of a polysurface, the Explode command will need to be used first.) 
5. Do this for all the walls, using different image outlines based on which type of building it is. 
