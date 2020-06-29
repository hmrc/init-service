package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.controllers

import org.scalatest.{Matchers, WordSpec}
import org.scalatestplus.play.guice.GuiceOneAppPerSuite
import play.api.{Configuration, Environment}
import play.api.http.Status
import play.api.test.Helpers._
import play.api.test.{FakeRequest, Helpers}
import uk.gov.hmrc.play.bootstrap.config.ServicesConfig
import uk.gov.hmrc.$!APP_PACKAGE_NAME!$.config.AppConfig

class MicroserviceHelloWorldControllerSpec extends WordSpec with Matchers with GuiceOneAppPerSuite {

  private val fakeRequest = FakeRequest("GET", "/")

  private val env           = Environment.simple()
  private val configuration = Configuration.load(env)

  private val serviceConfig = new ServicesConfig(configuration)
  private val appConfig     = new AppConfig(configuration, serviceConfig)

  private val controller = new MicroserviceHelloWorldController(appConfig, Helpers.stubControllerComponents())

  "GET /" should {
    "return 200" in {
      val result = controller.hello()(fakeRequest)
      status(result) shouldBe Status.OK
    }
  }
}
