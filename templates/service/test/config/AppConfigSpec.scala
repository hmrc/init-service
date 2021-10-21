package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.config

import org.scalatestplus.play.PlaySpec
import play.api.Configuration
<!--(if type=="BACKEND")-->
import uk.gov.hmrc.play.bootstrap.config.ServicesConfig
<!--(end)-->

class AppConfigSpec extends PlaySpec {

  private val mockConfiguration = Configuration(
  <!--(if type=="FRONTEND")-->
    "features.welsh-language-support" -> false
  <!--(end)-->
  <!--(if type=="BACKEND")-->
    "microservice.metrics.graphite.host" -> "graphite",
    "auditing.enabled" -> true,
    "microservice.services.auth.host" -> "localhost",
    "microservice.services.auth.port" -> 8500
  <!--(end)-->
  )

  <!--(if type=="BACKEND")-->
  private val mockServiceConfig = new ServicesConfig(mockConfiguration)

  lazy val appConfig = new AppConfig(mockConfiguration, mockServiceConfig)
  <!--(end)-->
  <!--(if type=="FRONTEND")-->
  lazy val appConfig = new AppConfig(mockConfiguration)
  <!--(end)-->

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
