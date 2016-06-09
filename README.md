# Play-Game-Services-Android-Module-for-Godot
Compile with Godot's source to get Google Play Game Services for Android in Godot up and running.

To use this module first you need to register your app with your Developer's Console. In "Linked Apps", you need to verify your app with a SHA1. So, that means you need to generate your release keystore first before anything else.

To do that, you need keytool.exe which can be found in your bin folder in your JDK folder. Put keytool.exe in a command prompt, then chdir or cd to the directory where you want your keystore file to be. Then generate it:

keytool -genkey -v -keystore **my-release-key.keystore** -alias **alias_name** -keyalg RSA -keysize 2048 -validity 10000

Replace my-release-key.keystore and alias_name with whatever you want to call your keystore file and alias_name.

After that you will be asked to type some details, and you will also be asked to type passwords. Remember these passwords. When it is all done, you should get a keystore file. Hold on to your keystore file for as long as you want your app to exist.

Now within the same directory that your newly generated my-release-key.keystore file is in, use keytool again like this:

keytool -list -v -keystore **my-release-key.keystore** -alias **alias_name** -storepass **mystorepassword** -keypass **mystorepassword**

Replace the ones in bold. And remember the passwords you typed just now? You need to type them here.

In the command prompt there should be a list of stuff, find the one that says "SHA1". Copy the entire SHA1 key (the numbers/letters separated by colons) then go back to your Developer's Console. And in "Linked Apps", find where you can put in your SHA1 key. Then submit and you should get your Applicaation ID.

Now clone or download this repo, in PlayGameServices/android/ there's a file AndroidManifestChunk.xml. Edit it in a text editor. On the first line you see this:

`<meta-data android:name="com.google.android.gms.games.APP_ID" android:value="\ [ADD APP ID HERE]" />`

So you want to type your Application ID there so that it looks like this:

`<meta-data android:name="com.google.android.gms.games.APP_ID" android:value="\ 552615016742" />`

Next go to [Godot's GitHub repo](https://github.com/godotengine/godot) and clone/download the sources.

Now you need to copy the entire PlayGameServices folder and put it in your godot-source/modules folder. Same place where gdscript and gridmap modules are. 

Now [compile Godot for Android](http://docs.godotengine.org/en/latest/reference/compiling_for_android.html). Make sure you have the requirements installed / set up. Open a Developer Command Prompt for Visual Studio with Administrator rights.

cd or chdir to the root folder of Godot's sources and type:

scons platform=android target=release tools=no android_arch=armv6 android_neon=no

Then wait for the compilation to be done. When it is done, go to the bin folder, there should be a libgodot...............so file. Rename this file to libgodot_android.so, then, within the Godot sources directory copy this file to platform/android/java/libs/armeabi. If libs/armeabi isn't there, you need to create it yourself. Now open up a command prompt and go to just platform/android/java and type:

gradlew.bat build

or

./gradlew build

Wait for it to be done, then go to platform/android/java/build/outputs/apk/ there should be 3 apks there. Get the one that says java-release......apk and rename it to android_release.apk and put it somewhere convenient for Godot.

Since this module works with release apks only we don't have to compile for Android in debug mode and get an android_debug.apk.

Now open Godot, and go to Scene -> Project Settings. At the very top, but just right below the tabs, you can see Category: and Properties: and Type:

So type "android" for Category: "modules" for Property: and set the Type: to string and click Add. You should get a new Android section in the list of Sections. Click on it, and there should be a "modules" field where you can type.

So type:

org/godotengine/godot/PlayGameServices 

in it and press enter. Now make a new gdscript file, put it on a Node in a scene or something.

In the gdscript file, you could do something like this:

```
var PlayGameServices = null

func _init():
	if Globals.has_singleton("PlayGameServices"):
		PlayGameServices = Globals.get_singleton("PlayGameServices")
		PlayGameServices.init(get_instance_ID())
```

Remember that right after you get_singleton("PlayGameServices") you must always use the init() method and pass get_instance_ID() into it before doing anything else with the module. Now here are some other functions that can be used in gdscript:

```
PlayGameServices.sign_in() 
PlayGameServices.sign_out()
PlayGameServices.leaderboard_submit(String id, int score)
PlayGameServices.leaderboard_show(String id)
PlayGameServices.achievement_unlock(String achievement_id)
PlayGameServices.achievement_increment(String achievement_id, int increment_amount)
PlayGameServices.achievement_show_list()
```

Note that to use leaderboards, you must have at least one leaderboard already created in your Developer's Console. Same goes with achievements. You will get your ID and all there too.

All these only works on a real Android system. So to test it, you need to export it into an Android apk and install it in your Android device. Remember to export it with your android_release.apk you compiled just now.