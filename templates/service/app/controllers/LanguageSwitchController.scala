package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.controllers

import com.google.inject.Inject
import javax.inject.Singleton
import play.api.Configuration
import play.api.i18n.{I18nSupport, Lang, MessagesApi}
import play.api.mvc._
import uk.gov.hmrc.play.bootstrap.frontend.controller.FrontendBaseController
import uk.gov.hmrc.$!APP_PACKAGE_NAME!$.config.AppConfig
import java.net.URL

@Singleton
class LanguageSwitchController @Inject()(configuration: Configuration,
                                         appConfig: AppConfig,
                                         override implicit val messagesApi: MessagesApi,
                                         val controllerComponents: MessagesControllerComponents
                                        ) extends FrontendBaseController with I18nSupport {

  private def fallbackURL: String = routes.HelloWorldController.helloWorld.url

  private def switchToLanguage(lang: Lang): Action[AnyContent] = Action { implicit request =>
    val redirectURL: String = request.headers.get(REFERER)
      .map(referrer => new URL(referrer)).map(_.getPath)
      .getOrElse(fallbackURL)

    if (appConfig.welshLanguageSupportEnabled) {
      Redirect(redirectURL).withLang(Lang.apply(lang.code))
    } else {
      Redirect(redirectURL)
    }
  }

  def switchToWelsh(): Action[AnyContent] = switchToLanguage(Lang("cy"))

  def switchToEnglish(): Action[AnyContent] = switchToLanguage(Lang("en"))
}

