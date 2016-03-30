import sbt._
import uk.gov.hmrc.SbtAutoBuildPlugin
import uk.gov.hmrc.sbtdistributables.SbtDistributablesPlugin
import uk.gov.hmrc.versioning.SbtGitVersioning
import play.PlayImport._
import play.core.PlayVersion

object MicroServiceBuild extends Build with MicroService {

  val appName = "$!APP_NAME!$"

  private val microserviceBootstrapVersion = "$!microserviceBootstrapVersion!$"
  private val playAuthVersion = "$!playAuthVersion!$"
  private val playHealthVersion = "$!playHealthVersion!$"
  private val playJsonLoggerVersion = "$!playJsonLoggerVersion!$"  
  private val playUrlBindersVersion = "$!playUrlBindersVersion!$"
  private val playConfigVersion = "$!playConfigVersion!$"
  private val domainVersion = "$!domainVersion!$"
  private val hmrcTestVersion = "$!hmrcTestVersion!$"
  <!--(if MONGO)-->
  private val playReactivemongoVersion = "$!playReactivemongoVersion!$"
  <!--(end)-->

  override lazy val plugins: Seq[Plugins] = Seq(
    SbtAutoBuildPlugin, SbtGitVersioning, SbtDistributablesPlugin
  )

  override lazy val appDependencies: Seq[ModuleID] = compile ++ testDependencies ++ itDependencies

  val compile = Seq(
    <!--(if MONGO)-->
    "uk.gov.hmrc" %% "play-reactivemongo" % playReactivemongoVersion,
    <!--(end)-->

    ws,
    "uk.gov.hmrc" %% "microservice-bootstrap" % microserviceBootstrapVersion,
    "uk.gov.hmrc" %% "play-authorisation" % playAuthVersion,
    "uk.gov.hmrc" %% "play-health" % playHealthVersion,
    "uk.gov.hmrc" %% "play-url-binders" % playUrlBindersVersion,
    "uk.gov.hmrc" %% "play-config" % playConfigVersion,
    "uk.gov.hmrc" %% "play-json-logger" % playJsonLoggerVersion,
    "uk.gov.hmrc" %% "domain" % domainVersion
  )

  val testDependencies: Seq[ModuleID] = baseTestDependencies("test")

  val itDependencies: Seq[ModuleID] = baseTestDependencies("it")

  private def baseTestDependencies(scope: String): Seq[ModuleID] = Seq(
    "uk.gov.hmrc" %% "hmrctest" % hmrcTestVersion % scope,
    "org.scalatest" %% "scalatest" % "2.2.2" % scope,
    "org.pegdown" % "pegdown" % "1.4.2" % scope,
    "org.jsoup" % "jsoup" % "1.7.3" % scope,
    "com.typesafe.play" %% "play-test" % PlayVersion.current % scope
  )

}
