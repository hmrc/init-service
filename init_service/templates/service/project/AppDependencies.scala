import play.core.PlayVersion
import play.sbt.PlayImport._
import sbt.Keys.libraryDependencies
import sbt._

object AppDependencies {

  private val bootstrapVersion = "$!bootstrapPlayVersion!$"
  <!--(if MONGO)-->private val hmrcMongoVersion = "$!mongoVersion!$"<!--(end)-->

  val compile = Seq(
    <!--(if type=="FRONTEND")-->
    "uk.gov.hmrc"             %% "bootstrap-frontend-play-30" % bootstrapVersion,
    "uk.gov.hmrc"             %% "play-frontend-hmrc-play-30" % "$!playFrontendHmrcVersion!$"<!--(if MONGO)-->,<!--(end)-->
    <!--(end)-->
    <!--(if type in ["BACKEND", "API"])-->
    "uk.gov.hmrc"             %% "bootstrap-backend-play-30"  % bootstrapVersion<!--(if MONGO)-->,<!--(end)-->
    <!--(end)-->
    <!--(if MONGO)-->
    "uk.gov.hmrc.mongo"       %% "hmrc-mongo-play-30"         % hmrcMongoVersion
    <!--(end)-->
  )

  val test = Seq(
    "uk.gov.hmrc"             %% "bootstrap-test-play-30"     % bootstrapVersion            % Test,
    <!--(if MONGO)-->"uk.gov.hmrc.mongo"       %% "hmrc-mongo-test-play-30"    % hmrcMongoVersion            % Test,<!--(end)-->
    <!--(if type=="FRONTEND")-->
    "org.jsoup"               %  "jsoup"                      % "1.13.1"            % Test,
    <!--(end)-->
  )

  val it = Seq.empty
}
