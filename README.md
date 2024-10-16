[![MSFS](./Documentation/images/msfs_logo.png)](https://www.flightsimulator.com/) [![Blender](./Documentation/images/blender_logo_socket.png)](https://www.blender.org/)

# LODs Easy Generator

This project was born to make life easier for Microsoft Flight Simulator aircraft developers (as I am) using Blender as the 3D development platform

One critical topic any Microsoft Flight Simulator aircraft developer must deal with is the creation of different levels of details (LODs) of the aircraft as this is required by the simulator in order to keep the impact on the performance as low as possible.
Normally this task is one of the latest in the aircraft development process as the LODs are created from the final version of the 3D model (the base full version) in order to avoid to repeat it after changes are applied

There are actually several freeware and payware add-ons available for Blender trying to make easier the creation of different level of details for the objects of a scene but they normally create copies of the involved meshes applying to them algorithms to reduce progressively their level of details: unfortunately this approach makes them useless for the development of an aircraft for Microsoft Flight Simulator as the mesh names are used throughout the implementation of the model behavior

To overcome this limitation I designed a workflow to implement (with a custom Blender add-on) an automatic process for LODs files creation taking in consideration this critical requirement but I didn't find anyone willing to develop it therefore I decided to develop it on my own

I should say I never created a custom Blender add-on before neither I knew how to program using Python language (the one required by Blender to develop custom extensions) but as I have a computer science background I accepted this challenge

Luckily there are a lot of Blender custom add-ons examples available just browsing the web and for any doubt I had during the development I found a lot of answers just looking for them with a good search engine

After a lot of trial and error attempts I finally have reached the result I was actually looking for (with some additional ideas I added during the development) and the **LODS Easy Generator** came to life: it is actually using the standard Blender Decimate modifier to reduce the level of details of the scene meshes.

:warning: Current version of the **LODs Easy Generator** addon is compatible with Blender version from **3.6.0**

:warning: This Blender add-on is provided free as it is therefore there is no guarantee of the result achieved or for any damage its use can cause (therefore make always a backup of your Blender file before using it)

**Note:** all my current payware aircraft creations for Microsoft Flight Simulator have been published on the in-game marketplace and [SimMarket](https://secure.simmarket.com/advanced_search_result.php?keywords=aerosachs) by AeroSachs 

# Add-on installation using Blender:

1. Go to the Releases section of the https://github.com/erasam/LODs-Easy-Generator repository, then download the zip file `lods-easy-generator.zip`.

![Download Release](Documentation/images/Releases.jpg)

2. Open Blender and go to : Edit > Preferences.

![Edit Preferences - Add](Documentation/images/Preferences.jpg)

3. Go to Add-ons and click on Install an add-on: this will bring up a file dialog where you navigate to the folder where you have your `lods-easy-generator.zip` downloaded file.

4. Select the `lods-easy-generator.zip` file and click on the Install Add-on button.

![Edit Preferences - Install](Documentation/images/AddonInstall.jpg)

5. Enable the Add-on by clicking on the checkbox.

![Edit Preferences - Enable](Documentation/images/AddonEnable.jpg)

# Documentation
You can read the detailed workflow I implemented in the included Documentation [here](./Documentation/Documentation.md)
