import sbt._
import uk.gov.hmrc.SbtAutoBuildPlugin
import uk.gov.hmrc.sbtdistributables.SbtDistributablesPlugin
import uk.gov.hmrc.versioning.SbtGitVersioning
import play.PlayImport._
import play.core.PlayVersion

object FrontendBuild extends Build with MicroService {

  val appName = "$!APP_NAME!$"

  private val playHealthVersion = "$!playHealthVersion!$"    
  private val playJsonLoggerVersion = "$!playJsonLoggerVersion!$"      
  private val frontendBootstrapVersion = "$!frontendBootstrapVersion!$"
  private val govukTemplateVersion = "$!govukTemplateVersion!$"
  private val playUiVersion = "$!playUiVersion!$"
  private val playPartialsVersion = "$!playPartialsVersion!$"
  private val playAuthorisedFrontendVersion = "$!playAuthorisedFrontendVersion!$"
  private val playConfigVersion = "$!playConfigVersion!$"
  private val hmrcTestVersion = "$!hmrcTestVersion!$"

  override lazy val plugins: Seq[Plugins] = Seq(
    SbtAutoBuildPlugin, SbtGitVersioning, SbtDistributablesPlugin
  )

  override lazy val appDependencies: Seq[ModuleID] = compile ++ testDependencies

  val compile = Seq(
    ws,
    "uk.gov.hmrc" %% "frontend-bootstrap" % frontendBootstrapVersion,
    "uk.gov.hmrc" %% "play-partials" % playPartialsVersion,
    "uk.gov.hmrc" %% "play-authorised-frontend" % playAuthorisedFrontendVersion,
    "uk.gov.hmrc" %% "play-config" % playConfigVersion,
    "uk.gov.hmrc" %% "play-json-logger" % playJsonLoggerVersion,
    "uk.gov.hmrc" %% "govuk-template" % govukTemplateVersion,
    "uk.gov.hmrc" %% "play-health" % playHealthVersion,
    "uk.gov.hmrc" %% "play-ui" % playUiVersion
  )

  val testDependencies: Seq[ModuleID] = baseTestDependencies("test")

  private def baseTestDependencies(scope: String): Seq[ModuleID] = Seq(
    "uk.gov.hmrc" %% "hmrctest" % hmrcTestVersion % scope,
    "org.scalatest" %% "scalatest" % "2.2.2" % scope,
    "org.pegdown" % "pegdown" % "1.4.2" % scope,
    "org.jsoup" % "jsoup" % "1.7.3" % scope,
    "com.typesafe.play" %% "play-test" % PlayVersion.current % scope
  )

}


