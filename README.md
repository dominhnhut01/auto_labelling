# Auto labelling using Background Substractor

## Table of Contents
1. [Main idea]
2. [Disadvantages]
3. [How to use]

## Main idea
The main idea of this script is because our dataset is collected by a static camera, we can use the background frames as a base to detect new object appearing in the frame. Moreover, because each animal in our dataset is already put in a different folder, we can label different classes only by detecting the object in the frames. For example, if we detect an object in folder fox, it must be a fox.

## How to use
1/ Put the images which have the same background in separate folder in "/dataset" directory
2/ Find an image containing only background and set its name to "background.<extension>"
3/ Run the script
4/ When two windows pop up, there will be trackbar for us to adjust the parameters. List of parameters in order:
- areaThreshold: 
