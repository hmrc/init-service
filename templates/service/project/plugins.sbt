resolvers += Resolver.url("HMRC Sbt Plugin Releases", url("https://dl.bintray.com/hmrc/sbt-plugin-releases"))(
  Resolver.ivyStylePatterns)

resolvers += "HMRC Releases" at "https://dl.bintray.com/hmrc/releases"

resolvers += Resolver.typesafeRepo("releases")

addSbtPlugin("uk.gov.hmrc" % "sbt-auto-build" % "$!sbt_auto_build!$")

addSbtPlugin("uk.gov.hmrc" % "sbt-git-versioning" % "$!sbt_git_versioning!$")

addSbtPlugin("uk.gov.hmrc" % "sbt-artifactory" % "$!sbt_artifactory!$")

addSbtPlugin("uk.gov.hmrc" % "sbt-distributables" % "$!sbt_distributables!$")

addSbtPlugin("com.typesafe.play" % "sbt-plugin" % "2.7.5")

addSbtPlugin("org.irundaia.sbt" % "sbt-sassify" % "1.4.11")
