# Keep Kotlinx serialization generated classes
-keepclassmembers class **$Companion { *; }
-keepclassmembers class kotlinx.serialization.** { *; }
-keepclassmembers class ** implements kotlinx.serialization.KSerializer { *; }
-dontwarn kotlinx.serialization.**