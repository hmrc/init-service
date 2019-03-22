import play.core.PlayVersion.current
import play.sbt.PlayImport._
import sbt.Keys.libraryDependencies
import sbt._

object AppDependencies {

  val compile = Seq(

    <!--(if type=="FRONTEND")-->
    "uk.gov.hmrc"             %% "govuk-template"           % "$!govukTemplateVersion!$",
    "uk.gov.hmrc"             %% "play-ui"                  % "$!playUiVersion!$",
    <!--(end)-->
    <!--(if MONGO)-->
    "uk.gov.hmrc"             %% "simple-reactivemongo"       % "$!simpleReactivemongoVersion!$",
    <!--(end)-->
    "uk.gov.hmrc"             %% "bootstrap-play-25"        % "$!bootstrapPlay25Version!$"
  )

  val test = Seq(
    "org.scalatest"           %% "scalatest"                % "3.0.4"                 % "test",
    <!--(if type=="FRONTEND")-->
    "org.jsoup"               %  "jsoup"                    % "1.10.2"                % "test",
    <!--(end)-->
    "com.typesafe.play"       %% "play-test"                % current                 % "test",
    "org.pegdown"             %  "pegdown"                  % "1.6.0"                 % "test, it",
    "uk.gov.hmrc"             %% "service-integration-test" % "0.2.0"                 % "test, it",
    "org.scalatestplus.play"  %% "scalatestplus-play"       % "2.0.0"                 % "test, it"
  )

}
