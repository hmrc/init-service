import sbt._

object LibDependencies {

  val compile = Seq(
  )

  lazy val test: Seq[ModuleID] = Seq(
    "org.scalatest"          %% "scalatest"    % "3.2.17" % Test,
    "com.vladsch.flexmark"   %  "flexmark-all" % "0.64.8" % Test
  )
}
