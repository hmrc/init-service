resolvers += "HMRC-open-artefacts-maven" at "https://open.artefacts.tax.service.gov.uk/maven2"
resolvers += Resolver.url("HMRC-open-artefacts-ivy", url("https://open.artefacts.tax.service.gov.uk/ivy2"))(Resolver.ivyStylePatterns)
resolvers += Resolver.typesafeRepo("releases")

addSbtPlugin("uk.gov.hmrc"       % "sbt-auto-build"     % "$!sbt_auto_build!$")
addSbtPlugin("uk.gov.hmrc"       % "sbt-git-versioning" % "$!sbt_git_versioning!$")
addSbtPlugin("uk.gov.hmrc"       % "sbt-distributables" % "$!sbt_distributables!$")
addSbtPlugin("com.typesafe.play" % "sbt-plugin"         % "2.8.7")
<!--(if type=="FRONTEND")-->
addSbtPlugin("com.typesafe.sbt"  % "sbt-gzip"           % "1.0.2")
addSbtPlugin("org.irundaia.sbt"  % "sbt-sassify"        % "1.5.1")
<!--(end)-->
