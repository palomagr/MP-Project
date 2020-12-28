The primary goal of readData is to take in the data from MultiTracker.py and interpret it for further use. Some examples include converting the data into a .csv, separating the file based on index, and eventually getting a list of directions for each of those indices.  
  
Here's the overall structure of readData.py:  
1. Open each of your video .txt files and separate them into individual files based on index. 
2. For each of the indices, get a list of directions where the index/agent moves. 
3. If desired, create a heatmap of where people have gone inside Machu Picchu. 
4. If desired, create a list of the most visited places based on this heatmap data. 

Here's what each of the primary methods in the code do, and how to use them: 
  
1. separate_file(filename):  
This takes in a filepath on your computer (must be a .txt, presumably the data from MultiTracker.py) and separates it into individual files for each index (0, 1, 2...).  
It then saves each of these files in the same folder as the original file.  
  
2. simplify(filename):  
This simplifies a file to a data point for every second, instead of every 1/24th of a second. It can be very useful if you don't want to see so many data points, you don't need them, or if you want simplicity for debugging.   
Simplify should be done after separate_file, or if there's only one index in the file.  
This is because it works by checking if a second is already in the file, and if it isn't, then it adds it. So if there are two indices at the same timestamp, it will not include the second one.  
  
3. get_directions(filename, numDirections):  
This function should also be called after separate, since we want to get the directions for one index/agent (for later use in Unity).  
When it reads the file of this index, it creates a list of directions and distance that they need to turn and then move forward by.  
The numDirections variable is the number of directions that you want to have - look at 'Angles Diagram.jpg' in the Dropbox for reference.  
This is used in Unity to give commands to the agent - "Turn by direction X, then move forward by Y amount." If the index doesn't move - within a limit; 0.5 meters is what it's at now - it lists "None".  
get_directions also stores the data to create the heatmap later.  
  
The rest of the functions are helper methods with thorough comments - things like drawing the heatmap, loading files, and creating a list of the most visited areas.  
  
! IMPORTANT !  
Filenames will need to be changed, since the ones in the code are from my (Kimmy's) computer. I figured it would be better to leave them in than to make generic folder names that may be misleading.  
If you want a minimum amount of work fixing these filenames, here's my setup: (I've also uploaded this all to the Dropbox)   
  
The UROP folder is at Users/ *kmcpherson* /Documents/UROP  
In that folder, I have various images of Machu Picchu for confirming paths, as well as a test file for the code (testfile.txt) if needed.   
Also in that folder, I have a folder named "Videos." In there, I have three folders: dj01, dj02, and dj08, as well as "Video Text Files".  
The first three correlate with the drone videos in the dropbox. Inside each folder, I have the videos of the free walkers, named "dj01_1, dj01_2, ..." as well as the group videos - "g01_1, g01_2, ..." This is where you can access each of the videos, and this is useful for if you're using MultiTracker.py.  
The fourth is where the text files for each of those videos are, and this is how you access those files to read in readData.py.  
  
