- delete pod
```bash
kubectl delete pods <pod> --grace-period=0 --force
kubectl patch pod <pod> -p '{"metadata":{"finalizers":null}}' # if hitting wall :(
```
- get config/secret
```bash
kubectl get secrets -n <namespace> <secret-name> -o yaml | yq '.metadata.annotations."kubectl.kubernetes.io/last-applied-configuration"' | jq -r | yq -y
```
- restart/rollout namespace's deployments
```bash
kubectl -n <namespace> rollout restart deploy
```