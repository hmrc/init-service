{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation {
  name = "init-service-shell";
  buildInputs = [pkgs.python27Full];
}
