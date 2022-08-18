import sbt._

val appName = "$!APP_NAME!$"

lazy val library = Project(appName, file("."))
  .settings(
    majorVersion := 0,
    scalaVersion := "$!SCALA_VERSION!$",
//  isPublicArtefact := true, // Uncomment if this is a public repository
    libraryDependencies ++= LibDependencies.compile ++ LibDependencies.test
  )
