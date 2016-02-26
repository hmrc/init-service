import sbt._

object StubServiceBuild extends Build with MicroService {
  import scala.util.Properties.envOrElse

  val appName = "$!APP_NAME!$"
  val appVersion = envOrElse("$!UPPER_CASE_APP_NAME_UNDERSCORE_ONLY!$_VERSION", "999-SNAPSHOT")

  override lazy val appDependencies: Seq[ModuleID] = AppDependencies()
}

private object AppDependencies {
  import play.PlayImport._
  import play.core.PlayVersion


  private val microserviceBootstrapVersion = "$!microserviceBootstrapVersion!$"
  private val playHealthVersion = "$!playHealthVersion!$"
  private val playConfigVersion = "$!playConfigVersion!$"
  private val hmrcTestVersion = "$!hmrcTestVersion!$"
  
  val compile = Seq(
    ws,
    "uk.gov.hmrc" %% "microservice-bootstrap" % microserviceBootstrapVersion,
    "uk.gov.hmrc" %% "play-health" % playHealthVersion,
    "uk.gov.hmrc" %% "play-config" % playConfigVersion,
    "uk.gov.hmrc" %% "play-json-logger" % "1.0.0"
  )

  trait TestDependencies {
    lazy val scope: String = "test"
    lazy val test : Seq[ModuleID] = ???
  }

  object Test {
    def apply() = new TestDependencies {
      override lazy val test = Seq(
        "uk.gov.hmrc" %% "hmrctest" % hmrcTestVersion % scope,
        "org.scalatest" %% "scalatest" % "2.2.2" % scope,
        "org.pegdown" % "pegdown" % "1.4.2" % scope,
        "com.typesafe.play" %% "play-test" % PlayVersion.current % scope
      )
    }.test
  }

  def apply() = compile ++ Test()
}


