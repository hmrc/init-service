package uk.gov.hmrc.hello

import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class HelloWorldSpec extends AnyWordSpec with Matchers {

  "HelloWorld" should {

    "say hello" in {
      HelloWorld.sayHello shouldBe "hello"
    }
  }
}
