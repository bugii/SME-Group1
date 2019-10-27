//Enable build scans on all builds of a project

plugins {
  id 'com.gradle.build-scan' version '3.0
}

// Accept the license agreement

buildScan{
  termsOfServiceUrl = 'https://gradle.com/terms-of-service'
  termsOfServiceAgree = 'yes'
}
// Enable build scans for all builds 

initscript {
    repositories {
        gradlePluginPortal()
    }

    dependencies {
        classpath 'com.gradle:build-scan-plugin:@scanPluginVersion@'
    }
}

rootProject {
    apply plugin: com.gradle.scan.plugin.BuildScanPlugin

    buildScan {
        termsOfServiceUrl = 'https://gradle.com/terms-of-service'
        termsOfServiceAgree = 'yes'
    }
}
