curl -L https://istio.io/downloadIstio | sh -
kubectl get all
kubectl delete ns projectcontour

./istioctl install --set profile=demo -y OR istioctl install --set profile=demo -y

kubectl label namespace bm1 istio-injection=enabled

openssl genrsa -out cluster.local.key 2048
openssl req -new -key cluster.local.key -out cluster.local.csr
openssl x509 -req -days 3650 -in cluster.local.csr -signkey cluster.local.key -out cluster.local.crt
ls

rm cluster.local.csr
kubectl create -n istio-system secret tls wildcard-credential --key=cluster.local.key --cert=cluster.local.crt 
