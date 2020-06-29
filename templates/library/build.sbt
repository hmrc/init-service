import sbt._

val appName = "$!APP_NAME!$"

lazy val library = Project(appName, file("."))
  .enablePlugins(SbtAutoBuildPlugin, SbtGitVersioning, SbtArtifactory)
  .settings(
    majorVersion := 0,
    scalaVersion := "$!SCALA_VERSION!$",
//    makePublicallyAvailableOnBintray := true, // Uncomment if this is a public repository
    libraryDependencies ++= AppDependencies.compile ++ AppDependencies.test
  )
