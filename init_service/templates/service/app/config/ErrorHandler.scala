package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.config

import javax.inject.{Inject, Singleton}

import play.api.i18n.MessagesApi
import play.api.mvc.RequestHeader
import play.twirl.api.Html
import uk.gov.hmrc.play.bootstrap.frontend.http.FrontendErrorHandler
import uk.gov.hmrc.$!APP_PACKAGE_NAME!$.views.html.ErrorTemplate

import scala.concurrent.{ExecutionContext, Future}

@Singleton
class ErrorHandler @Inject()(
  errorTemplate: ErrorTemplate,
  override val messagesApi: MessagesApi
)(implicit override val ec: ExecutionContext
) extends FrontendErrorHandler {

  override def standardErrorTemplate(pageTitle: String, heading: String, message: String)(implicit request: RequestHeader): Future[Html] =
    Future.successful(errorTemplate(pageTitle, heading, message))
}
