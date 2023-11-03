curl -L https://istio.io/downloadIstio | sh -
kubectl get all
kubectl delete ns projectcontour

./istioctl install --set profile=demo -y OR istioctl install --set profile=demo -y

kubectl label namespace bmi istio-injection=enabled

openssl genrsa -out bmgo.local.key 2048
openssl req -new -key bmgo.local.key -out bmgo.local.csr
openssl x509 -req -days 3650 -in bmgo.local.csr -signkey bmgo.local.key -out bmgo.local.crt
ls

rm bmgo.local.key
##rm bmgo.local.csr
kubectl create -n istio-system secret tls wildcard-credential --key=bmgo.local.key --cert=bmgo.local.crt 
