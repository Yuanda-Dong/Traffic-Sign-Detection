# How to create model in Blender #

## Sign model: ##
![1.png](https://bitbucket.org/repo/G6xBMXK/images/90468248-1.png)
 
For all models, firstly create a new file. This contains a camera, a cube and a light. 

 ![2.png](https://bitbucket.org/repo/G6xBMXK/images/1178242865-2.png)
Remove all objects in the scene from the collection. 

 ![3.png](https://bitbucket.org/repo/G6xBMXK/images/2897970416-3.png)
Add mesh, for example, if we are making a sign, just create a plane. 

 ![4.png](https://bitbucket.org/repo/G6xBMXK/images/489108348-4.png)
From the plane modifier, generate a solidify modifier. 

 ![5.png](https://bitbucket.org/repo/G6xBMXK/images/3120764481-5.png)
Solidify modifier enables us to add thickness to the signs. 


 ![6.png](https://bitbucket.org/repo/G6xBMXK/images/2569805021-6.png)
From the world property, add node for the surface. Because we generated sign image already, just add image texture to the basic colour. 
 
![7.png](https://bitbucket.org/repo/G6xBMXK/images/2291344867-7.png)
Import the image we already created. 

 ![8.png](https://bitbucket.org/repo/G6xBMXK/images/1867880978-8.png)
Adjust the orientation, size of the signs. 
 
![9.png](https://bitbucket.org/repo/G6xBMXK/images/552691681-9.png)
Create a cylinder as the pole of the sign. Adjusted the signs and orientation of the pole. Combine the objects we created. 

 
![10.png](https://bitbucket.org/repo/G6xBMXK/images/673649815-10.png)
Addition of the signs: Because the image texture is two sides, we need to add an identical plane to the plane we have. So the sign will show as one side. 

## Track model: ##

 ![11.png](https://bitbucket.org/repo/G6xBMXK/images/2403666469-11.png)
F1 Track model is similar to the sign. Create a plane with the right scale as the track image (how to create a track image is written in the F1 track Unity documentation). Add the image texture through the node property just like for the sign model. 

## Other model, for example stadium:
 ##
![12.png](https://bitbucket.org/repo/G6xBMXK/images/940139439-12.png)
Create a basic stadium model from blender tutorial. Import chair model as fbx. 

 ![13.png](https://bitbucket.org/repo/G6xBMXK/images/80103449-13.png)
Duplicate the chair model and change the orientation of the chairs model. Add them to the stadium

 ![14.png](https://bitbucket.org/repo/G6xBMXK/images/1542413456-14.png)
Challenges: There are too many chair models with too many dimensions, which makes the file extremely large. This issue is resolved through reduce the dimensions of the mesh. 
Modeling -> Vertex -> Remove double vertices Modeling -> Mesh -> Clean up -> Delete loose Modeling -> Mesh -> Clean up -> Decimate geometry -> Drag to desired 'percentage' -> 0.1
 
![15.png](https://bitbucket.org/repo/G6xBMXK/images/2218166201-15.png)
Modify the surface and colour of the stadium. Blender and Unity differentiate in the surface object, which make some surfaces available in blender but not in Unity. We fixed this by using the available surface from both sides (collaborate with Mouyi Xu), and manually re-enter the hexadecimal of the colour in Unity. 

 ![16.png](https://bitbucket.org/repo/G6xBMXK/images/4079477598-16.png)
The final look of the stadium.
