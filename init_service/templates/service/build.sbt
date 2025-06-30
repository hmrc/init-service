import uk.gov.hmrc.DefaultBuildSettings

ThisBuild / majorVersion := 0
ThisBuild / scalaVersion := "$!SCALA_VERSION!$"
ThisBuild / scalacOptions += "-Wconf:msg=Flag.*repeatedly:s"

lazy val microservice = Project("$!APP_NAME!$", file("."))
  .enablePlugins(play.sbt.PlayScala, SbtDistributablesPlugin)
  .disablePlugins(JUnitXmlReportPlugin) //Required to prevent https://github.com/scalatest/scalatest/issues/1427
  .settings(
    libraryDependencies ++= AppDependencies.compile ++ AppDependencies.test,
    // https://www.scala-lang.org/2021/01/12/configuring-and-suppressing-warnings.html
    // suppress warnings in generated routes files
    scalacOptions += "-Wconf:src=routes/.*:s",
    <!--(if type=="FRONTEND")-->
    scalacOptions += "-Wconf:msg=unused import&src=html/.*:s",
    pipelineStages := Seq(gzip),
    <!--(end)-->
  )
  .settings(CodeCoverageSettings.settings: _*)
  <!--(if type=="API")-->
  .settings(
    Compile / unmanagedResourceDirectories += baseDirectory.value / "resources",
  )
  <!--(end)-->

lazy val it = project
  .enablePlugins(PlayScala)
  .dependsOn(microservice % "test->test")
  .settings(DefaultBuildSettings.itSettings())
  .settings(libraryDependencies ++= AppDependencies.it)
