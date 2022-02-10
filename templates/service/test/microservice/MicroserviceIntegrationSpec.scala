package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.microservice

import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.play.guice.GuiceOneAppPerSuite
import play.api.Application
import play.api.inject.guice.GuiceApplicationBuilder
import uk.gov.hmrc.$!APP_PACKAGE_NAME!$.config.AppConfig

class MicroserviceIntegrationSpec extends AnyWordSpec with Matchers with GuiceOneAppPerSuite {

  override def fakeApplication(): Application =
    new GuiceApplicationBuilder()
      .configure(
        "metrics.jvm"     -> false,
        "metrics.enabled" -> false
      )
      .build()

  "Microservice" should {
    "parse configuration without failure" in {
      val config = app.injector.instanceOf[AppConfig]
      config.appName shouldBe "$!APP_NAME!$"
    }
  }
}
