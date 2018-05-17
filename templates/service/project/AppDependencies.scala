import play.core.PlayVersion
import play.sbt.PlayImport._
import sbt.Keys.libraryDependencies
import sbt._

object AppDependencies {

  def appDependencies: Seq[Setting[_]] = Seq(
    libraryDependencies ++= compile ++ test()
  )

  val compile = Seq(
    <!--(if type=="FRONTEND")-->
    "uk.gov.hmrc" %% "govuk-template" % "$!govukTemplateVersion!$",
    "uk.gov.hmrc" %% "play-ui" % "$!playUiVersion!$",
    <!--(end)-->
    <!--(if MONGO)-->
    "uk.gov.hmrc" %% "play-reactivemongo" % "$!playReactivemongoVersion!$",
    <!--(end)-->
    ws,
    "uk.gov.hmrc" %% "bootstrap-play-25" % "$!bootstrapPlay25Version!$"
  )

  def test(scope: String = "test") = Seq(
    "uk.gov.hmrc" %% "hmrctest" % "$!hmrcTestVersion!$" % scope,
    "org.scalatest" %% "scalatest" % "3.0.0" % scope,
    "org.pegdown" % "pegdown" % "1.6.0" % scope,
    <!--(if type=="FRONTEND")-->
    "org.jsoup" % "jsoup" % "1.10.2" % scope,
    <!--(end)-->

    "com.typesafe.play" %% "play-test" % PlayVersion.current % scope
  )

}
