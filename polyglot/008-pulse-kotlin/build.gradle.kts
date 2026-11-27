plugins {
    id("com.android.application") version "8.7.3"
    kotlin("android") version "2.0.21"
}
android {
    namespace = "limiar.pulse"
    compileSdk = 35
    defaultConfig {
        applicationId = "limiar.pulse"
        minSdk = 23
        targetSdk = 35
        versionCode = 1
        versionName = "0.1"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}
dependencies { testImplementation("junit:junit:4.13.2") }
