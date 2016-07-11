# Play-Game-Services-Android-Module-for-Godot
**This is an _[Android module](http://docs.godotengine.org/en/latest/reference/creating_android_modules.html)_ for the [Godot](https://godotengine.org/) game engine to enable Google Play Services in Android builds.**

#### Features

Leaderboards |  Achievements
---------------|---------------
Submit scores. | Unlock achievements.
Show leaderboards. | Increment achievements.
                   | Show achievements.



## 1. Generate Release Keystore File

To use this module first you need to register your app with your _**[Developer's Console](https://play.google.com/apps/publish)**_. 

In your _**Developer's Console**_, go to _**Game Services**_ and ***Add new game***.

Then in your newly added game, go to  _**Linked Apps**_. You need to verify your app with a _**SHA1**_. So, that means you need to generate your release keystore first before continuing.

Use _**keytool.exe**_ which can be found in your _**bin**_ folder in your JDK folder. Run _**keytool.exe**_ from a command prompt, then ``chdir`` or ``cd`` to the directory where you want your keystore file to be. Generate it:

``keytool -genkey -v -keystore ``**`` my-release-key.keystore``**`` -alias ``**``alias_name``**`` -keyalg RSA -keysize 2048 -validity 10000``

Replace **``my-release-key.keystore``** and **``alias_name``** with whatever you want to call your **keystore file** and **alias_name**.

After that you will be asked to type some details, then passwords. Remember these passwords. When it is all done, you should get a keystore file. Hold on to your keystore file for as long as you want your app to exist.


## 2. Get SHA1 Key and then Application ID


Now within the same directory that your newly generated ***my-release-key.keystore*** file is in, use ***keytool.exe*** again like this:

``keytool -list -v -keystore ``**``my-release-key.keystore``**`` -alias ``**``alias_name``**`` -storepass ``**``mystorepassword``**`` -keypass ``**``mykeypassword``**

Replace the ones in bold with your own. And remember *the passwords you typed just now*? You need to type them here.

In the command prompt there should be a list of stuff, find the one that says __SHA1__. 

**Copy the entire SHA1 key** (the numbers/letters separated by colons) then go back to your ***Developer's Console***. And in ***Linked Apps***, find where you can put in your **SHA1** key. Then submit and you should get your **Application ID**. Note it down somewhere.


## 3. Clone This Repo and Paste Your Application ID Into AndroidManifestChunk.xml

Now clone or download this repo into your own computer, in ***PlayGameServices/android/*** there's a file ***AndroidManifestChunk.xml***. Edit it in a text editor. On the first line you see this:

`<meta-data android:name="com.google.android.gms.games.APP_ID" android:value="\ [ADD APP ID HERE]" />`

So you want to type your Application ID there so that it looks like this:

`<meta-data android:name="com.google.android.gms.games.APP_ID" android:value="\ 552615016742" />`


## 4. Modify config.py

Edit ***PlayGameServices/config.py*** in a text editor. Find the line that says:

``env.android_add_default_config("applicationId 'com.godot.game'")``

replace ``com.godot.game`` with your own. For example:

``env.android_add_default_config("applicationId 'com.ranmaru90.fours'")``

**Skipping this step will result in your Android app crashing horribly at startup.**


## 5. Clone Godot's Repo and Prepare This Module with Godot's Sources for Compilation

Next go to [Godot's GitHub repo](https://github.com/godotengine/godot) and clone / download Godot's sources.

Copy the entire ***PlayGameServices*** folder and put it in your ***\<godot-source\>/modules*** folder. Same folder/directory where ***gdscript*** and ***gridmap*** modules are. 

Now [compile Godot for Android](http://docs.godotengine.org/en/latest/reference/compiling_for_android.html). Make sure you have the requirements installed / set up. 


## 6. Compile

I'm using Windows so, I can only tell you to open a ***Developer Command Prompt for Visual Studio*** with *Administrator* rights.

``cd`` or ``chdir`` to the ***root folder of Godot's sources*** and type:

``scons platform=android target=release tools=no android_arch=armv6 android_neon=no``

Then wait for the compilation to be done. When it is done, go to the ***\<godot-source\>/platform/android/java*** folder. Now open up a command prompt in the same folder ***\<godot-source\>/platform/android/java*** and type:

``gradlew.bat build``

or

``./gradlew build``

Wait for it to be done, then go to ***\<godot-source\>/bin*** and you should see a file called ***android_release.apk***. This apk file is your Android release export template.

Since this module works with release apks only we don't have to compile for Android in debug mode and get an android_debug.apk.


## 7. Use the Module

Now open Godot, and go to ***Scene*** -> ***Project Settings***. At the very top, but just right below the tabs, you can see ***Category:*** and ***Properties:*** and ***Type:***

Type ***android*** for Category: ***modules*** for Property: and set the Type: to ***string*** and click Add. You should get a new Android section in the list of Sections. Click on it, and there should be a ***modules*** field where you can type.

So type:

``org/godotengine/godot/PlayGameServices`` 

in it and press enter. Now make a new gdscript file, put it on a Node in a scene or something.

In the gdscript file, you could do something like this:

```
var PlayGameServices = null

func _init():
	if Globals.has_singleton("PlayGameServices"):
		PlayGameServices = Globals.get_singleton("PlayGameServices")
		PlayGameServices.init(get_instance_ID())
```

Remember that right after you ``get_singleton("PlayGameServices")`` you must always use the ``init()`` method and pass ``get_instance_ID()`` into it before doing anything else with the module. 

Now here are some other functions that can be used in GDScript:

```
PlayGameServices.sign_in() 
PlayGameServices.sign_out()
PlayGameServices.leaderboard_submit(String id, int score)
PlayGameServices.leaderboard_show(String id)
PlayGameServices.achievement_unlock(String achievement_id)
PlayGameServices.achievement_increment(String achievement_id, int increment_amount)
PlayGameServices.achievement_show_list()
```

## 8. Exporting an Android Game to a Release apk

#### A. Editor Settings

When you're done with all that coding, you probably want to export it to an Android release apk. In Godot, go to ***Settings***. It's on the top-right corner. Then click on ***Editor Settings*** to bring it up.

Make sure you're in the ***General*** tab, under ***Sections***, click ***Android*** to reveal the engine-wide Android settings. Set the path to your ***adb.exe*** (found in your ***\<android-sdk\>/platform-tools/***) and ***jarsigner.exe*** (found in your ***\<jdk\>/bin/***). **.exe* if you're on Windows, of course.


Next, set the path to your ***debug keystore*** (Google for it if you don't know how to make one) and fill in the relevant details.

For ***Timestamping Authority URL*** you can fill it with ``http://timestamp.digicert.com/``

Close the dialog box after that.


#### B. Project Export Settings

Now click on the ***Export*** button. It's on the top-left corner. The ***Project Export Settings*** dialog box is brought up. Make sure you are on the ***Target*** tab, under ***Export to Platform***, click on ***Android***.

The ***Options*** are revealed. 

Since we're making an Android release apk, we have to make sure that ***Debugging Enabled*** is **unchecked**.

Under ***Custom Package*** set the path to your **Android release template** (***android_release.apk***) that you've compiled just now. Then under ***Package***, set the ***Unique Name***, make sure it's the same as the one you've done in ***Step 4***. Here, you can also give your Android game a ***Name***.

Let's go to ***Keystore***. In ***Release***, set the path to the **keystore file** you've generated in ***Step 1***. Then type in your ***Release User*** which is the same as ***alias_name*** in ***Step 2*** and ***Release Password*** which is the same as ***mystorepassword*** in ***Step 2***.

Under ***Permissions*** make sure ***Access Network State*** and ***Internet*** are **checked**.

Now you can click on the ***Export...*** button, give your apk file a name, and export the Android release apk. Install this apk on your Android device.


## 9. Miscellaneous Things to Take Note

* If you don't do this, even when your Android device is connected, it might keep trying to sign in to Google Play Services.
 	* In your ***Developer's Console***, under ***Game Details***, there's a tiny section at the bottom titled ***API Console Project***. Then there's: 
 	>This game is linked to the API console project called '***Your Game***'. 
 	>
 
 	* Click on **_Your Game_** and you'll be led to another page. Then click _**Enabled APIs**_ and see if all the APIs are **enabled** for your game.

* Note that to use leaderboards, **you must have at least one leaderboard already created in your _Developer's Console_**. **Same goes with achievements**. You will get your IDs and all there too.


* All these only work on **an actual Android system (a _device_ or _emulator_)**. So to test it, you need to **export** it into an Android **apk** and **install it in your Android device**. 


* Remember to **export it with your _android_release.apk_** you compiled just now.


* For **each app** that you want to add this module to, you need to do **Step 3** and **Step 4**, specific to your app. Then copy and paste and replace the entire ***PlayGameServices*** folder/directory in ***\<godot-source\>/modules***, follow through the steps and compile everything again. **So, you are *NOT* able to share one Android release template (*android_release.apk*) across all your Android games. You have to recompile for each Android app, since each app has its own unique Application ID and package name.** 
