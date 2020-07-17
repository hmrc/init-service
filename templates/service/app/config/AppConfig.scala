package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.config

import javax.inject.{Inject, Singleton}
import play.api.Configuration
import uk.gov.hmrc.play.bootstrap.config.ServicesConfig

@Singleton
class AppConfig @Inject()(config: Configuration, servicesConfig: ServicesConfig) {
<!--(if type=="FRONTEND")-->
  val footerLinkItems: Seq[String] = config.getOptional[Seq[String]]("footerLinkItems").getOrElse(Seq())

  val welshLanguageSupportEnabled: Boolean = config.getOptional[Boolean]("features.welsh-language-support").getOrElse(false)
<!--(end)-->

<!--(if type=="BACKEND")-->
  val authBaseUrl: String = servicesConfig.baseUrl("auth")

  val auditingEnabled: Boolean = config.get[Boolean]("auditing.enabled")
  val graphiteHost: String     = config.get[String]("microservice.metrics.graphite.host")
<!--(end)-->
}
