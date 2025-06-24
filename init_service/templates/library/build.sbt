import sbt._

lazy val library = Project("$!APP_NAME!$", file("."))
  .settings(
    majorVersion := 0,
    scalaVersion := "$!SCALA_VERSION!$",
//  isPublicArtefact := true, // Uncomment if this is a public repository
    libraryDependencies ++= LibDependencies.compile ++ LibDependencies.test
  )
