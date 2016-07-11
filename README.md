# Play-Game-Services-Android-Module-for-Godot
Compile with Godot's source to get Google Play Game Services for Android in Godot up and running.

### 1. Generate Relese Keystore File

To use this module first you need to register your app with your _**Developer's Console**_. 

In _**Linked Apps**_, you need to verify your app with a _**SHA1**_. So, that means you need to generate your release keystore first before anything else.

Use _**keytool.exe**_ which can be found in your _**bin**_ folder in your JDK folder. Run _**keytool.exe**_ from a command prompt, then ``chdir`` or ``cd`` to the directory where you want your keystore file to be. Generate it:

``keytool -genkey -v -keystore ``**`` my-release-key.keystore``**`` -alias ``**``alias_name``**`` -keyalg RSA -keysize 2048 -validity 10000``

Replace **``my-release-key.keystore``** and **``alias_name``** with whatever you want to call your **keystore file** and **alias_name**.

After that you will be asked to type some details, then passwords. Remember these passwords. When it is all done, you should get a keystore file. Hold on to your keystore file for as long as you want your app to exist.

---

### 2. Get SHA1 Key and Then Application ID


Now within the same directory that your newly generated ***my-release-key.keystore*** file is in, use ***keytool.exe*** again like this:

``keytool -list -v -keystore ``**``my-release-key.keystore``**`` -alias ``**``alias_name``**`` -storepass ``**``mystorepassword``**`` -keypass ``**``mykeypassword``**

Replace the ones in bold with your own. And remember *the passwords you typed just now*? You need to type them here.

In the command prompt there should be a list of stuff, find the one that says __SHA1__. 

**Copy the entire SHA1 key** (the numbers/letters separated by colons) then go back to your ***Developer's Console***. And in ***Linked Apps***, find where you can put in your **SHA1** key. Then submit and you should get your **Application ID**. Note it down somewhere.

---

### 3. Clone This Repo and Paste Your Application ID Into AndroidManifestChunk.xml

Now clone or download this repo into your own computer, in ***PlayGameServices/android/*** there's a file ***AndroidManifestChunk.xml***. Edit it in a text editor. On the first line you see this:

`<meta-data android:name="com.google.android.gms.games.APP_ID" android:value="\ [ADD APP ID HERE]" />`

So you want to type your Application ID there so that it looks like this:

`<meta-data android:name="com.google.android.gms.games.APP_ID" android:value="\ 552615016742" />`

---

### 4. Modify config.py

Edit ***PlayGameServices/config.py*** in a text editor. Find the line that says:

``env.android_add_default_config("applicationId 'com.godot.game'")``

replace ``com.godot.game`` with your own. For example:

``env.android_add_default_config("applicationId 'com.ranmaru90.fours'")``

**Skipping this step will result in your Android app crashing horribly at startup.**

---

### 5. Clone Godot's Repo and Prepare This Module with Godot's Sources for Compilation

Next go to [Godot's GitHub repo](https://github.com/godotengine/godot) and clone / download Godot's sources.

Copy the entire ***PlayGameServices*** folder and put it in your ***\<godot-source\>/modules*** folder. Same folder/directory where ***gdscript*** and ***gridmap*** modules are. 

Now [compile Godot for Android](http://docs.godotengine.org/en/latest/reference/compiling_for_android.html). Make sure you have the requirements installed / set up. 

---

### 6. Compile

I'm using Windows so, I can only tell you to open a ***Developer Command Prompt for Visual Studio*** with *Administrator* rights.

``cd`` or ``chdir`` to the ***root folder of Godot's sources*** and type:

``scons platform=android target=release tools=no android_arch=armv6 android_neon=no``

Then wait for the compilation to be done. When it is done, go to the ***\<godot-source\>/platform/android/java*** folder. Now open up a command prompt in the same folder ***\<godot-source\>/platform/android/java*** and type:

``gradlew.bat build``

or

``./gradlew build``

Wait for it to be done, then go to ***\<godot-source\>/bin*** and you should see a file called ***android_release.apk***. This apk file is your Android release export template.

Since this module works with release apks only we don't have to compile for Android in debug mode and get an android_debug.apk.

---

### 7. Use the Module

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

Now here are some other functions that can be used in gdscript:

```
PlayGameServices.sign_in() 
PlayGameServices.sign_out()
PlayGameServices.leaderboard_submit(String id, int score)
PlayGameServices.leaderboard_show(String id)
PlayGameServices.achievement_unlock(String achievement_id)
PlayGameServices.achievement_increment(String achievement_id, int increment_amount)
PlayGameServices.achievement_show_list()
```

### 8. Miscellaneous Things to Take Note

* Note that to use leaderboards, **you must have at least one leaderboard already created in your Developer's Console**. **Same goes with achievements**. You will get your IDs and all there too.


* All these only work on **an actual Android system (a _device_ or _emulator_)**. So to test it, you need to **export** it into an Android **apk** and **install it in your Android device**. 


* Remember to **export it with your _android_release.apk_** you compiled just now.


* One more thing, if you don't do this, even when your Android device is connected, it might keep trying to sign in to Google Play Services.
 	* In your developer's console, under "Game Details", there's a tiny section at the bottom titled "API Console Project". Then there's: 
 	>This game is linked to the API console project called 'Your Game'. 
 	>
 
 	* Click on **_Your Game_** and you'll be led to another page. Then click _**Enabled APIs**_ and see if all the APIs are **enabled** for your game.