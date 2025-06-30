package uk.gov.hmrc.$!APP_PACKAGE_NAME!$.controllers

import play.api.mvc.{Action, AnyContent, ControllerComponents}
import controllers.Assets
import uk.gov.hmrc.play.bootstrap.backend.controller.BackendController

import javax.inject.{Inject, Singleton}

@Singleton
class DocumentationController @Inject() (
  assets: Assets,
  cc: ControllerComponents
) extends BackendController(cc):

  def definition(): Action[AnyContent] =
    assets.at("/public/api", "definition.json")

  def specification(version: String, file: String): Action[AnyContent] =
    assets.at(s"/public/api/conf/$version", file)
