def can_build(plat):
    return plat == 'android'

def configure(env):
	if env['platform'] == 'android':
		env.android_add_dependency("compile 'com.google.android.gms:play-services-games:+'")
		env.android_add_dependency("compile 'com.google.android.gms:play-services-plus:+'")
		env.android_add_to_manifest("android/AndroidManifestChunk.xml")
		env.android_add_java_dir("android/src/")
		env.android_add_default_config("applicationId 'com.godot.game'")
		env.disable_module()