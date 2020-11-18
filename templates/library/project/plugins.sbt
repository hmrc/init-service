resolvers += Resolver.bintrayIvyRepo("hmrc", "sbt-plugin-releases")
resolvers += Resolver.bintrayRepo("hmrc", "releases")
resolvers += Resolver.typesafeRepo("releases")

addSbtPlugin("uk.gov.hmrc" % "sbt-auto-build"     % "$!sbt_auto_build!$")
addSbtPlugin("uk.gov.hmrc" % "sbt-git-versioning" % "$!sbt_git_versioning!$")
addSbtPlugin("uk.gov.hmrc" % "sbt-artifactory"    % "$!sbt_artifactory!$")