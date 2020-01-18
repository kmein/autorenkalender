{ buildPythonPackage, requests, ... }:
buildPythonPackage {
  pname = "autorenkalender";
  version = "0.1.2";
  src = ./.;
  propagatedBuildInputs = [ requests ];
}
