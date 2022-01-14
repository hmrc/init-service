package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.controllers

import uk.gov.hmrc.$!APP_PACKAGE_NAME!$.config.AppConfig
import uk.gov.hmrc.play.bootstrap.backend.controller.BackendController
import play.api.mvc.{Action, AnyContent, ControllerComponents}
import javax.inject.{Inject, Singleton}
import scala.concurrent.Future

@Singleton()
class MicroserviceHelloWorldController @Inject()(appConfig: AppConfig, cc: ControllerComponents)
    extends BackendController(cc) {

  def hello(): Action[AnyContent] = Action.async { implicit request =>
    Future.successful(Ok(s"Hello ${appConfig.appName}"))
  }
}
