package uk.gov.hmrc.$!APP_PACKAGE_NAME!$

import play.api.{Configuration, Environment}
import play.api.inject.{Binding, Module => AppModule}

import java.time.Clock

class Module extends AppModule:

  override def bindings(
    environment  : Environment,
    configuration: Configuration
  ): Seq[Binding[_]] =
    bind[Clock].toInstance(Clock.systemDefaultZone) :: // inject if current time needs to be controlled in unit tests
    Nil
