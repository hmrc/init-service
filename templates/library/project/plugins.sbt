resolvers += Resolver.url("hmrc-sbt-plugin-releases", url("https://dl.bintray.com/hmrc/sbt-plugin-releases"))(
  Resolver.ivyStylePatterns)

resolvers += "HMRC Releases" at "https://dl.bintray.com/hmrc/releases"

addSbtPlugin("uk.gov.hmrc" % "sbt-auto-build" % "$!sbt_auto_build!$")

addSbtPlugin("uk.gov.hmrc" % "sbt-git-versioning" % "$!sbt_git_versioning!$")

addSbtPlugin("uk.gov.hmrc" % "sbt-artifactory" % "$!sbt_artifactory!$")