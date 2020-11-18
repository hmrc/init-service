resolvers += Resolver.bintrayIvyRepo("hmrc", "sbt-plugin-releases")
resolvers += Resolver.bintrayRepo("hmrc", "releases")
resolvers += Resolver.typesafeRepo("releases")

addSbtPlugin("uk.gov.hmrc"       % "sbt-auto-build"     % "$!sbt_auto_build!$")
addSbtPlugin("uk.gov.hmrc"       % "sbt-git-versioning" % "$!sbt_git_versioning!$")
addSbtPlugin("uk.gov.hmrc"       % "sbt-distributables" % "$!sbt_distributables!$")
addSbtPlugin("com.typesafe.play" % "sbt-plugin"         % "2.7.5")
<!--(if type=="FRONTEND")-->
addSbtPlugin("org.irundaia.sbt"  % "sbt-sassify"        % "1.4.11")
<!--(end)-->
