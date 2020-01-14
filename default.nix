{ buildPythonPackage, requests, ... }:
buildPythonPackage {
  pname = "autorenkalender";
  version = "0.1.0";
  src = ./.;
  propagatedBuildInputs = [ requests ];
}
