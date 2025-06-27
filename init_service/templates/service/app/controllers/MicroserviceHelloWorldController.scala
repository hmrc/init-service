package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.controllers

import play.api.mvc.{Action, AnyContent, ControllerComponents}
import uk.gov.hmrc.play.bootstrap.backend.controller.BackendController

import javax.inject.{Inject, Singleton}

@Singleton()
class MicroserviceHelloWorldController @Inject()(
  cc: ControllerComponents
) extends BackendController(cc):

  val hello: Action[AnyContent] =
    Action:
      implicit request =>
        Ok("Hello world")
