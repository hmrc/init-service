let
  bootstrap = import <nixpkgs> {};
  nixpkgs   = bootstrap.fetchFromGitHub (bootstrap.lib.importJSON ./nixpkgs.json);
  pkgs      = import nixpkgs { };
in
  pkgs.mkShell {
    buildInputs = [
      pkgs.python39Packages.virtualenv
    ];
    shellHook = ''
      virtualenv venv
      source ./venv/bin/activate
      pip install poetry
      make init
    '';
  }
