import play.core.PlayVersion.current
import play.sbt.PlayImport._
import sbt.Keys.libraryDependencies
import sbt._

object AppDependencies {

  val compile = Seq(
    <!--(if type=="FRONTEND")-->
    "uk.gov.hmrc"             %% "bootstrap-frontend-play-27" % "$!bootstrapPlay27Version!$",
    "uk.gov.hmrc"             %% "govuk-template"             % "$!govukTemplateVersion!$",
    "uk.gov.hmrc"             %% "play-ui"                    % "$!playUiVersion!$"<!--(if MONGO)-->,<!--(end)-->
    <!--(end)-->
    <!--(if type=="BACKEND")-->
    "uk.gov.hmrc"             %% "bootstrap-backend-play-27"  % "$!bootstrapPlay27Version!$"<!--(if MONGO)-->,<!--(end)-->
    <!--(end)-->
    <!--(if MONGO)-->
    "uk.gov.hmrc"             %% "simple-reactivemongo"       % "$!simpleReactivemongoVersion!$"
    <!--(end)-->
  )

  val test = Seq(
    "uk.gov.hmrc"             %% "bootstrap-test-play-27"   % "$!bootstrapPlay27Version!$" % Test,
    "org.scalatest"           %% "scalatest"                % "3.1.2"                 % Test,
    <!--(if type=="FRONTEND")-->
    "org.jsoup"               %  "jsoup"                    % "1.10.2"                % Test,
    <!--(end)-->
    "com.typesafe.play"       %% "play-test"                % current                 % Test,
    "com.vladsch.flexmark"    %  "flexmark-all"             % "0.35.10"               % "test, it",
    "org.scalatestplus.play"  %% "scalatestplus-play"       % "4.0.3"                 % "test, it"
  )
}
