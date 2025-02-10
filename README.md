# cloud-hybride

infra :
- gateway :           10.1.1.1/24
- srv-vcenter :       10.1.1.2/24
- srv-esxi01 :        10.1.1.3/24
- srv-esxi01 :        10.1.1.4/24
- srv-portail :       10.1.1.5/24
- srv-api :           10.1.1.6/24
- srv-conteneur :     10.1.1.8/24
- srv-bdd :           10.1.1.9/24
- srv-orchestrator :  10.1.1.10/24
- server-kube-work01 :  10.1.1.11/24
- server-kube-work02 :  10.1.1.12/24
- server-kube-master :  10.1.1.13/24
- server-web :        10.1.1.41/24

service :
- srv-vcenter :       vcenter-client
- srv-esxi01 :        hyperviseur esxi
- srv-esxi01 :        hyperviseur esxi
- srv-portail :       flask
- srv-api :           fastapi
- srv-conteneur :     docker
- srv-bdd :           mariadb
- srv-orchestrator :  terraform + ansible
- server-kube-work01 :  kubernetes
- server-kube-work02 :  kubernetes
- server-kube-master :  kubernetes
- server-web :        nginx / traefik
