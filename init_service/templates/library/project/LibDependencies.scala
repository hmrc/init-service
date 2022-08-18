import sbt._

object LibDependencies {

  val compile = Seq(
  )

  lazy val test: Seq[ModuleID] = Seq(
    "org.pegdown"            %  "pegdown"      % "1.6.0"  % Test,
    "org.scalatest"          %% "scalatest"    % "3.2.5"  % Test,
    "com.vladsch.flexmark"   %  "flexmark-all" % "0.36.8" % Test
  )

}
