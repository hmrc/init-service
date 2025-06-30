package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.controllers

import play.api.mvc.{Action, AnyContent, MessagesControllerComponents}
import uk.gov.hmrc.$!APP_PACKAGE_NAME!$.views.html.HelloWorldPage
import uk.gov.hmrc.play.bootstrap.frontend.controller.FrontendController

import javax.inject.{Inject, Singleton}

@Singleton
class HelloWorldController @Inject()(
  mcc: MessagesControllerComponents,
  helloWorldPage: HelloWorldPage
) extends FrontendController(mcc):

  val helloWorld: Action[AnyContent] =
    Action:
      implicit request =>
        Ok(helloWorldPage())
