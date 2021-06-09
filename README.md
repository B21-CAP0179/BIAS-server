# Body-Imaging-Anomaly-Scanner

Capstone Project Bangkit Program 2021

PeduliLindungi-ID is a mobile application that can detect whether there is any disease within a patient body through images.

- Coding Language : Kotlin
- minimal SDK version : 21

dependencies {

    implementation "org.jetbrains.kotlin:kotlin-stdlib:$kotlin_version"
    implementation 'androidx.core:core-ktx:1.5.0'
    implementation 'androidx.appcompat:appcompat:1.3.0'
    implementation 'com.google.android.material:material:1.3.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.0.4'
    implementation 'com.google.firebase:firebase-auth:19.2.0'
    implementation 'com.google.firebase:firebase-firestore:23.0.0'
    implementation 'androidx.legacy:legacy-support-v4:1.0.0'
    implementation 'de.hdodenhof:circleimageview:2.1.0'
    implementation 'com.google.firebase:firebase-storage:20.0.0'
    testImplementation 'junit:junit:4.+'
    androidTestImplementation 'androidx.test.ext:junit:1.1.2'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.3.0'
    implementation 'com.github.bumptech.glide:glide:4.12.0'
    annotationProcessor 'com.github.bumptech.glide:compiler:4.12.0'
}


How to replicate our application:
1. Build model exploration so we can use it for the web server
2. Downloading and saving the model use for the prediction image
3. Build webserver using Flask
4. Preparing dockerfile to build docker image 
5. Preparing container registry for docker image 
6. Pushing docker image to Container registry
7. Preparing Cloud Run for deploying image from container registry
8. Preparing Cloud build for automatic deployment so we can use continues deployment
9. Preparing Firestore/Firebase for the database
10. Design the Android Application
11. Connect Firestore/Firebase to the Android Studio
