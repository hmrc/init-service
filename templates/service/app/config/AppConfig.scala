package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.config

import javax.inject.{Inject, Singleton}
import play.api.Configuration
import play.api.i18n.Lang
import uk.gov.hmrc.play.bootstrap.config.ServicesConfig

@Singleton
class AppConfig @Inject()(config: Configuration, servicesConfig: ServicesConfig) {
<!--(if type=="FRONTEND")-->
  val welshLanguageSupportEnabled: Boolean = config.getOptional[Boolean]("features.welsh-language-support").getOrElse(false)

  val en: String            = "en"
  val cy: String            = "cy"
  val defaultLanguage: Lang = Lang(en)
<!--(end)-->

<!--(if type=="BACKEND")-->
  val authBaseUrl: String = servicesConfig.baseUrl("auth")

  val auditingEnabled: Boolean = config.get[Boolean]("auditing.enabled")
  val graphiteHost: String     = config.get[String]("microservice.metrics.graphite.host")
<!--(end)-->
}
