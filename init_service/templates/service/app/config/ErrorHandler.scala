package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.config

import play.api.i18n.MessagesApi
import play.api.mvc.RequestHeader
import play.twirl.api.Html
import uk.gov.hmrc.play.bootstrap.frontend.http.FrontendErrorHandler
import uk.gov.hmrc.$!APP_PACKAGE_NAME!$.views.html.ErrorTemplate

import scala.concurrent.{ExecutionContext, Future}
import javax.inject.{Inject, Singleton}

@Singleton
class ErrorHandler @Inject()(
  errorTemplate: ErrorTemplate,
  val messagesApi: MessagesApi
)(using
  val ec: ExecutionContext
) extends FrontendErrorHandler:

  override def standardErrorTemplate(
    pageTitle: String,
    heading: String,
    message: String
  )(implicit request: RequestHeader): Future[Html] =
    Future.successful(errorTemplate(pageTitle, heading, message))
