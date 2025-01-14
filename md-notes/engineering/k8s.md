- delete resources (like pod, deployment, service, ...)
```bash
kubectl delete pods pod-name --grace-period=0 --force
kubectl patch pod pod-name -p '{"metadata":{"finalizers": []}}' --type=merge # if hitting wall :(
```
- get config/secret
```bash
kubectl get secrets -n namespace secret-name -o yaml | yq '.metadata.annotations."kubectl.kubernetes.io/last-applied-configuration"' | jq -r | yq -y
kubectl get secrets -n namespace secret-name -o go-template='{{range $k,$v := .data}}{{printf "%s: " $k}}{{if not $v}}{{$v}}{{else}}{{$v | base64decode}}{{end}}{{"\n"}}{{end}}'
```
- restart/rollout namespace's deployments, replicasets, ...
```bash
kubectl -n namespace rollout restart deployment/deployment-name
```