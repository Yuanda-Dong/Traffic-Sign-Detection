# How to Create a F1 track and car model
CP32_W17B_Group1
## PDF
The [pdf file](https://drive.google.com/drive/folders/14gcG4-uwHYuvHbr_MX3mJ-RGb2JcMLyS?usp=sharing) of this documentation was uploaded to Google Drive.
## Tools:
Photoshop, Blender, Unity
## Map:
You should first find an image of your track. 

![figure 1.png](https://bitbucket.org/repo/G6xBMXK/images/3626276724-figure%201.png)

Create a new .psd file and import the image into it.

Then create path using pen tool and trace the whole track on the image.

![2.png](https://bitbucket.org/repo/G6xBMXK/images/3062757998-2.png)

Remove the origin image and check the track under the path column (working path).

![3.png](https://bitbucket.org/repo/G6xBMXK/images/4052083020-3.png)

Press F5 to open the brush setting.

![4.png](https://bitbucket.org/repo/G6xBMXK/images/1019998692-4.png)

Set the size to some appropriate number related to the width of the track.

We set our track to 400 pixels

Also, set the colour on the up-left corner to white(Hex: f2f2f2).

![5.png](https://bitbucket.org/repo/G6xBMXK/images/731385056-5.png)

Right-click your path. And click “stroke path”.

Then choose to use brush tool to stroke.

![6.png](https://bitbucket.org/repo/G6xBMXK/images/3031780948-6.png)

Click “confirm” and you will see a wide path as shown.

This will be outer white margin of the track.

![7.png](https://bitbucket.org/repo/G6xBMXK/images/506117350-7.png)

Repeat the above action twice to draw the track and the middle yellow line.

For the track, we set the width to 350 pixels and the color to grey (Hex: 666666)

For the middle yellow line, we set the width to 20 pixels and the color to yellow (Hex: FFE100)

Finally, we will see the track path.

![8.png](https://bitbucket.org/repo/G6xBMXK/images/4062194837-8.png)

Now, we need a background texture.

First, add a background layer.

Then use painting tool to add a grass texture.

![9.png](https://bitbucket.org/repo/G6xBMXK/images/303328677-9.png)

Export the picture as JPG file and import it into Unity.

Change the following import settings:

- Max Size : 8192
- Compression: High Quality

![10.png](https://bitbucket.org/repo/G6xBMXK/images/789022343-10.png)

Create an Object as a track and put the picture as a texture on it.

Please refer to the documentation [Map_and_Sign_Implementation](https://drive.google.com/file/d/1aEYqoVVhaFHwdkCK5FofWWGykba2cUPz/view) from CP31 on how to build the track.

The only changes are the size of the track and the texture.

![11.png](https://bitbucket.org/repo/G6xBMXK/images/1960482379-11.png)

![12.png](https://bitbucket.org/repo/G6xBMXK/images/427168086-12.png)

Then you can create some 3D object such as the fence alongside the track using blender and put them on the track as part of the environment.

That’s all steps for building the map. The next thing is to build the car model.

## Car Model

First build a car model in Blender and export as a .fbx file.

Refer to [Blender Documentation](https://bitbucket.org/RobertJia/comp3988_t17b_group1/wiki/Blender%20documentation) for further information on how to build a model in Blender.

You can use the Windows 3D Picture Viewer to check if the .fbx file contains all the textures.

![13.png](https://bitbucket.org/repo/G6xBMXK/images/2068520664-13.png)

Create a folder with your car’s name under the Models folder. Here, we use `SF1000` as the name.

Then import the .fbx file by clicking `import new Asset`.

![14.png](https://bitbucket.org/repo/G6xBMXK/images/3776315622-14.png)

Now go to prefabs folder and drag the “donkey” prefab to your current scene.

![15.png](https://bitbucket.org/repo/G6xBMXK/images/4257135089-15.png)

Then drag the donkey in Hierarchy back to the prefab folder.

After doing this, there will be a notification.

![16.png](https://bitbucket.org/repo/G6xBMXK/images/3830230572-16.png)

Click `original prefab` and Unity will create a prefab for you in the prefab folder.

Also, don’t forget to delete the donkey in your current scene.

![17.png](https://bitbucket.org/repo/G6xBMXK/images/424195767-17.png)

Open the new prefab.

![18.png](https://bitbucket.org/repo/G6xBMXK/images/1054128921-18.png)

Delete the unnecessary stuff in the donkey car

- All objects under donkey except car name mount
- The pcCube under cameraSensor
- Wheels under tireRR, tireRL, tireFL, tireFR

![19.png](https://bitbucket.org/repo/G6xBMXK/images/3991348594-19.png)

Drag the car model into the prefab.

![20.png](https://bitbucket.org/repo/G6xBMXK/images/1516855475-20.png)

Set the position of the car model based on the `fake ground shadow`.

![21.png](https://bitbucket.org/repo/G6xBMXK/images/2735029892-21.png)

Right click the car model and choose `unpack prefab`.

![22.png](https://bitbucket.org/repo/G6xBMXK/images/2959167842-22.png)

Find out the four tires.

![23.png](https://bitbucket.org/repo/G6xBMXK/images/3193053473-23.png)

Drag them out of the prefab and record their positions.

Set the position of wheelParents (under wheelMeshes) to be the same as the position of their corresponding tires.

e.g. the position of wheelRRParent should be the same as the position of the backward right tire

![24.png](https://bitbucket.org/repo/G6xBMXK/images/4251852900-24.png)

After modify the position, move the tires under the corresponding tire object

- The forward left tire under tireFL
- The forward right tire under tireFR
- The backward left tire under tireRL
- The backward right tire under tireRR

![25.png](https://bitbucket.org/repo/G6xBMXK/images/3339811722-25.png)

Change the position of the four tireColliders (under wheelsCol) to be the same as the corresponding wheelParents

![26.png](https://bitbucket.org/repo/G6xBMXK/images/2457923611-26.png)

Select the car model and add a `box collider` component.

![27.png](https://bitbucket.org/repo/G6xBMXK/images/353386756-27.png)

Change the size of the box.

![28.png](https://bitbucket.org/repo/G6xBMXK/images/408384740-28.png)

Select layers and click add layers.

![29.png](https://bitbucket.org/repo/G6xBMXK/images/529383615-29.png)

Type in a new layer called `My Car`.

![30.png](https://bitbucket.org/repo/G6xBMXK/images/1976461559-30.png)

Change the layer from `Default` to `MyCar`.

![31.png](https://bitbucket.org/repo/G6xBMXK/images/3775112097-31.png)

Select `Yes, change children`.

![32.png](https://bitbucket.org/repo/G6xBMXK/images/347639246-32.png)

Now, go to camera sensor and unselect MyCar from Culling Mark.

![33.png](https://bitbucket.org/repo/G6xBMXK/images/1938187703-33.png)

Save your prefab and go back to the f1 track scene.

Choose `Car Spawner` and change `Car Prefab` to your newly made prefab.

![34.png](https://bitbucket.org/repo/G6xBMXK/images/3924267941-34.png)

Now you can build the simulator and have your F1 track with new car model.
