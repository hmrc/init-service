package uk.gov.hmrc.$!APP_PACKAGE_NAME!$

import org.scalatest.concurrent.{IntegrationPatience, ScalaFutures}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import org.scalatestplus.play.guice.GuiceOneServerPerSuite
import play.api.Application
import play.api.inject.guice.GuiceApplicationBuilder
import scala.concurrent.ExecutionContext.Implicits.global
import uk.gov.hmrc.http.client.HttpClientV2
import uk.gov.hmrc.http.{StringContextOps, HttpReads, HeaderCarrier}
import uk.gov.hmrc.http.HttpReads.Implicits.readRaw

class HealthEndpointIntegrationSpec
  extends AnyWordSpec
     with Matchers
     with ScalaFutures
     with IntegrationPatience
     with GuiceOneServerPerSuite:

  private val httpClient = app.injector.instanceOf[HttpClientV2]
  private val baseUrl  = s"http://localhost:$port"

  override def fakeApplication(): Application =
    GuiceApplicationBuilder()
      .build()

  "service health endpoint" should:
    "respond with 200 status" in:
      val response =
        httpClient
          .get(url"$baseUrl/ping/ping")(HeaderCarrier())
          .execute()
          .futureValue

      response.status shouldBe 200
