# Blender-CSPBrushImporter
Blender Plugin that imports SUT brushes to blender as a texture brush

## How to Use

#### The Addon will appear in the texture panel as "CSP Brush Import Panel"

![image](https://user-images.githubusercontent.com/56279192/213882901-77aecd2d-2d69-4eb3-a9e9-d916059a902d.png)

#### Once the button is pressed, look for the .sut file that you would like to convert (make sure there are no '.'s in the name as that will cause a few minor errors right now ).

![image](https://user-images.githubusercontent.com/56279192/213882962-dae057c6-6302-436c-a3ec-f43291bfebf7.png)

#### Once selected, a .png file of the brush texture is also generated and placed in the same diretory as the .sut file that was selected.

![image](https://user-images.githubusercontent.com/56279192/213883040-b221c247-0d1e-4bd2-ba2a-b04559d81ef2.png)

#### Also, a new texture brush will be created with a few modified settings from the default with the name of the file.

![image](https://user-images.githubusercontent.com/56279192/213883058-8e3d0c83-9b5a-4778-9a0f-ff0b13580418.png)

#### Currently there is an error that has to be worked around manually where the png cannot load properly. This problem is addressed in the "Issues" section.


## Issues


<details>
<summary>PNG Fails To Automatically Load Into Blender</summary>
<p align="center">

#### Currently Blender does not like the way the PNG is saved by the addon and will give an error in the texture panel.

![image](https://user-images.githubusercontent.com/56279192/213882352-7e8f5c63-6472-4159-9c40-fa3430dcc373.png)

#### This is currently fixed by saving a copy over the original image then reloading the image from the texture panel
#### Make sure to save over ther original with the same name

![image](https://user-images.githubusercontent.com/56279192/213882557-a1c19153-b5c8-4e0f-a564-ba0cb9ca5064.png)

#### Back in Blender hitting the refresh Icon will reload the image and should remove the error

![image](https://user-images.githubusercontent.com/56279192/213882801-21cedf41-3abe-47ad-9a05-19f58478b040.png)
  


</p>
</details>



