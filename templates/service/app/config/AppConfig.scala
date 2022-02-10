package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.config

import javax.inject.{Inject, Singleton}
import play.api.Configuration

@Singleton
class AppConfig @Inject()(config: Configuration) {
<!--(if type=="FRONTEND")-->
  val welshLanguageSupportEnabled: Boolean = config.getOptional[Boolean]("features.welsh-language-support").getOrElse(false)
<!--(end)-->

<!--(if type=="BACKEND")-->
  val appName: String = config.get[String]("appName")
<!--(end)-->
}
