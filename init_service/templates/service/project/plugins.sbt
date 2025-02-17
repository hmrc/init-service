resolvers += MavenRepository("HMRC-open-artefacts-maven2", "https://open.artefacts.tax.service.gov.uk/maven2")
resolvers += Resolver.url("HMRC-open-artefacts-ivy2", url("https://open.artefacts.tax.service.gov.uk/ivy2"))(Resolver.ivyStylePatterns)
resolvers += Resolver.typesafeRepo("releases")

addSbtPlugin("uk.gov.hmrc"        % "sbt-auto-build"     % "$!sbt_auto_build!$")
addSbtPlugin("uk.gov.hmrc"        % "sbt-distributables" % "$!sbt_distributables!$")
addSbtPlugin("org.playframework"  % "sbt-plugin"         % "3.0.6")
addSbtPlugin("org.scoverage"      % "sbt-scoverage"      % "2.0.12")
<!--(if type=="FRONTEND")-->
addSbtPlugin("com.github.sbt"     % "sbt-gzip"           % "2.0.0")
addSbtPlugin("uk.gov.hmrc"        % "sbt-sass-compiler"  % "$!sbt_sass_compiler!$")
<!--(end)-->
