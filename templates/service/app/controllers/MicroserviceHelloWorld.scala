package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.controllers

import javax.inject.{Inject, Singleton}

import scala.concurrent.ExecutionContext
import uk.gov.hmrc.play.bootstrap.controller.BaseController
import play.api.mvc._

import scala.concurrent.Future

@Singleton()
class MicroserviceHelloWorld @Inject() (implicit ec : ExecutionContext) extends BaseController {

	def hello() = Action.async { implicit request =>
		Future.successful(Ok("Hello world"))
	}

}
