package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.config

import org.scalamock.scalatest.MockFactory
import org.scalatestplus.play.PlaySpec
import play.api.{ConfigLoader, Configuration}
<!--(if type=="BACKEND")-->
import uk.gov.hmrc.play.bootstrap.config.ServicesConfig
<!--(end)-->

class AppConfigSpec extends PlaySpec with MockFactory {

  private val mockConfiguration = mock[Configuration]

  <!--(if type=="FRONTEND")-->
  (mockConfiguration.getOptional(_: String)(_: ConfigLoader[Boolean]))
    .expects("features.welsh-language-support", *)
    .returns(Some(false))
  <!--(end)-->

  <!--(if type=="BACKEND")-->
  (mockConfiguration.get(_: String)(_: ConfigLoader[String]))
    .expects("microservice.metrics.graphite.host", *)
    .returns("graphite")

  (mockConfiguration.get(_: String)(_: ConfigLoader[Boolean]))
    .expects("auditing.enabled", *)
    .returns(true)

  private val mockServiceConfig = mock[ServicesConfig]

  (mockServiceConfig.baseUrl(_: String))
    .expects("auth")
    .returns("http://localhost:8500")
  <!--(end)-->

  lazy val appConfig = new AppConfig(
    mockConfiguration
    <!--(if type=="BACKEND")-->
    , mockServiceConfig
    <!--(end)-->
    )

  "AppConfig" should {
    <!--(if type=="FRONTEND")-->
    "return the welshLanguageSupportEnabled flag" in {
      appConfig.welshLanguageSupportEnabled mustBe false
    }
    <!--(end)-->
    <!--(if type=="BACKEND")-->
    "return the authBaseUrl" in {
      appConfig.authBaseUrl mustBe "http://localhost:8500"
    }

    "return the graphiteHost" in {
      appConfig.graphiteHost mustBe "graphite"
    }

    "return auditingEnabled flag" in {
      appConfig.auditingEnabled mustBe true
    }
    <!--(end)-->
  }
}
