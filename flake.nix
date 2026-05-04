{
  description = "pixi development environment for pl-dcm2niix";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        lib = pkgs.lib;
        fhs = pkgs.buildFHSEnv ({
          name = "pixi";
          targetPkgs = pkgs: with pkgs; [ pixi ];
          runScript = "pixi shell";
        });
      in {
        devShells.default = fhs.env;
      });
}
