1. setup GKE cluster
- using [terraform module](https://github.com/terraform-google-modules/terraform-google-kubernetes-engine)
2. connect to gke cluster
	[GCP doc](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl)
	- install [kubectl](https://kubernetes.io/docs/tasks/tools/), [gcloud-cli](https://cloud.google.com/sdk/docs/install-sdk) and `gke-gcloud-auth-plugin` 
```bash
gcloud container clusters get-credentials k8s-cluster --region=asia-southeast1 # if regional cluster
gcloud container clusters get-credentials staging-k8s-cluster --zone=asia-southeast1-a # if zonal cluster
```
3. create new namespace and change current namespace to seperate environments
```bash
kubectl create namespace mmenu-prod
kubectl config set-context --current --namespace mmenu-prod # change current namespace to 'mmenu-prod'
```
4. create service account for GKE deployment
- create `gke-cluster-deployment` service account with 2 roles:
	- `Artifact Registry Writer` for create and push docker images and helm charts
	- `Kubernetes Engine Developer` for GKE deployment using helm
- create new JSON credentials for new service account and add Gitlab CICD variables
	- `GKE_CICD_SA=gke-cluster-deployment@mmenu-api-prod.iam.gserviceaccount.com`
	- `GKE_CICD_SA_KEY=xxx` (with base64 encoded credentials: `base64 /path/to/creadentials.json -w0`)
5. setup artifact registry (local)
	- create `docker` and `helm` repos for pushing docker images and helm charts
	- run `gcloud auth configure-docker asia-southeast1-docker.pkg.dev` to allow docker/helm push to registry
	- docker/helm:
```bash
docker push asia-southeast1-docker.pkg.dev/mmenu-api-prod/docker/<image name>:<image tag>
helm push <chart.tgz> oci://asia-southeast1-docker.pkg.dev/mmenu-api-prod/helm
```
6. create helm chart and deploy to GKE
- example for `mmenu-api` application
- create helm chart
```bash
helm create mmenu-api
```
	and remove `mmenu-api/templates/tests
- edit `values.yaml`
```yaml
# Default values for mmenu-api.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

image:
  repository: asia-southeast1-docker.pkg.dev`/mmenu-api-prod/docker/mmenu-api # docker image url for pulling
  pullPolicy: IfNotPresent # or Always
  # Overrides the image tag whose default is the chart appVersion.
  tag: "latest" # latest if not specified

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

# neednt create service account
serviceAccount:
  # Specifies whether a service account should be created
  create: false
  # Annotations to add to the service account
  annotations: {}
  # The name of the service account to use.
  # If not set and create is true, a name is generated using the fullname template
  name: ""

podAnnotations: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  type: ClusterIP # or NodePort, LoadBalancer (is NodePort and create GCP NLB)
  port: 3000  # application port

# enable if using container-native load balancing (classical ALB or internal ALB) with ingress
ingress:
  enabled: true
  className: ""
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
    kubernetes.io/ingress.class: "gce-internal" # enable internal ingress
    kubernetes.io/ingress.regional-static-ip-name: "mmenu-api-internal-ip" # terraform
  hosts: []
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

# for horizontal auto scaling
# k8s converts CPU to CPU shares, 1 CPU = 1024 shares ~ 1000m
resources:
  # We usually recommend not to specify default resources and to leave this as a conscious
  # choice for the user. This also increases chances charts run on environments with little
  # resources, such as Minikube. If you do want to specify resources, uncomment the following
  # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
  limits:
	# cpu: 1000m # 1 CPU, neednt set limits for CPU
	memory: 128Mi
  requests:
    cpu: 100m # if request is too high, k8s cannot find appropriate node for deployment
	memory: 128Mi # need set memory's limits and requests are same value, k8s need delete pod for memory reclamation

autoscaling:
  enabled: true
  minReplicas: 1 # HPA scales pods within [minReplicas, maxReplicas]
  maxReplicas: 100
  # targetCPUUtilizationPercentage is limits' percentage * (resources' limits / resources' requests)
  targetCPUUtilizationPercentage: 500 # will be scaled when cpu is 5x of requests (500m)
  # targetMemoryUtilizationPercentage: 80
  # scale up velocity: 5 pods in 10 seconds
  scaleUpPods: 5
  scaleUpDurationInSeconds: 10

nodeSelector: {}

tolerations: []

affinity: {}

```
- replace `hpa.yaml` (to support GKE)
```yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "mmenu-api.fullname" . }}
  labels:
    {{- include "mmenu-api.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "mmenu-api.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
    {{- end }}
    {{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetMemoryUtilizationPercentage }}
    {{- end }}
  # if want to adjust scaling up velocity, set value for `scaleUpPods` and `scaleUpDurationInSeconds` in `values.yaml`
  {{- if .Values.autoscaling.scaleUpPods }}
  behavior:
    scaleUp:
      policies:
        - type: Pods
          value: {{ .Values.autoscaling.scaleUpPods }}
          periodSeconds: {{ .Values.autoscaling.scaleUpDurationInSeconds | default 15 }}
  {{- end }}
{{- end }}
```
- edit `deployment.yaml` to import environment variables and mount volumes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mmenu-api.fullname" . }}
  labels:
    {{- include "mmenu-api.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels: # for selecting and managing pods
      {{- include "mmenu-api.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "mmenu-api.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "mmenu-api.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          command: ["npm", "run", "start"]
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /v2/healthCheck # route to health check
              port: http # name of exposed port above
            # if grpc application
            # grpc:
            #   port: {{ .Values.service.port }}
            # if TCP
		    # tcpSocket:
		    #   port: http
          readinessProbe:
            httpGet:
              path: /v2/healthCheck # route to health check
              port: http # name of exposed port above
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          # import environment variables from configmap or secret (cannot be seen)
          envFrom:
            {{- if .Values.configEnv }}
            - configMapRef:
                name: {{ .Values.configEnv }} # set value in `values.yaml` or helm command
            {{- end }}
            {{- if .Values.secretEnv }}
            - secretRef:
                name: {{ .Values.secretEnv }} # set value in `values.yaml` or helm command
            {{- end }}
          # volumes can be mounted using configmap
	      # volumeMounts: []
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}

```
- create or edit `backendconfig.yaml` for service (if not using HTTP healthcheck)
```yaml
apiVersion: cloud.google.com/v1
kind: BackendConfig
metadata:
  name: {{ include "mmenu-api.fullname" . }}
spec:
  healthCheck:
    type: HTTP # support HTTP, HTTP2, TCP, gRPC, ...
    requestPath: /v2/healthCheck # health check route (no authentication)
    port: {{ .Values.service.port }}
  cdn:
    enabled: false # enable cdn or not (neccessary for frontend applications)
    cachePolicy:
      includeHost: true
      includeProtocol: true
      includeQueryString: false
  securityPolicy: # enable cloud armor for external ingress or gateway (created by terraform)
    name: {{ .Values.caPolicy | default "" }} # name of cloud armor policy (terraform)

```
- edit `service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "mmenu-api.fullname" . }}
  labels:
    {{- include "mmenu-api.labels" . | nindent 4 }}
  annotations:
    cloud.google.com/neg: '{"ingress": true}' # Creates a NEG after an Ingress is created (added by GCP automatically)
    cloud.google.com/backend-config: '{"default": "{{ include "mmenu-api.fullname" . }}"}' # remove this line if not set backendconfig for service
spec:
  type: {{ .Values.service.type }}
  # can set static ip for loadBalancerIP or clusterIP by name (created by terraform)
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "mmenu-api.selectorLabels" . | nindent 4 }}
```
- we have 2 ways for deploying service
	- using gateway (recommended)
		- routings are defined in `Gateway` and `HTTPRoute` configs. we can create only 1 ALB (gateway) for all services.
		- supports certificate-manager (wildcard domains)
		- add `Gateway` (if not exists) and `HTTPRoute`
```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: Gateway
metadata:
  name: external-http-gateway
  namespace: mmenu-prod
  annotations:
    networking.gke.io/certmap: mmenu-io-certmap
spec:
  # see gke gateway capabilities at https://cloud.google.com/kubernetes-engine/docs/how-to/gatewayclass-capabilities
  gatewayClassName: gke-l7-global-external-managed
  addresses:
    - type: NamedAddress
      value: prod-external-http-gateway-ip # external static ip (terraform)
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: Same # restrict httproutes' http to gateway's namespace
    - name: https
      protocol: HTTPS
      port: 443
---
# https redirect
apiVersion: gateway.networking.k8s.io/v1beta1
kind: HTTPRoute
metadata:
  name: https-redirect
  namespace: mmenu-prod
spec:
  parentRefs:
    - name: external-http-gateway
      kind: Gateway
      sectionName: http # listener's name
  rules:
    - filters:
      - type: RequestRedirect
        requestRedirect:
          scheme: https
---
# mmenu-api
# currently, GKE's HTTPRoute doesnt support regex matching
apiVersion: gateway.networking.k8s.io/v1beta1
kind: HTTPRoute
metadata:
  name: mmenu-api
  namespace: mmenu-prod
spec:
  parentRefs:
    - name: external-http-gateway
      kind: Gateway
  hostnames:
    - api.mmenu.io
  rules:
    - backendRefs: # match all paths
      - name: mmenu-api
        port: 3000
---
apiVersion: gateway.networking.k8s.io/v1beta1
kind: HTTPRoute
metadata:
  name: mmenu-admin-production
  namespace: mmenu-prod
spec:
  parentRefs:
    - name: external-http-gateway
      kind: Gateway
  hostnames:
    - shop.mmenu.io
  rules:
    - matches:
      - path:
          type: PathPrefix
          value: /main.dart.js
      filters:
        - type: RequestRedirect
          requestRedirect:
            hostname: d5fgok2ro4am6.cloudfront.net
            path:
              type: ReplacePrefixMatch
              replacePrefixMatch: '/website/web/mmenu-admin/version/20231220_042801/main.dart.js' # redirect to cdn
            statusCode: 301
    - backendRefs: # match all paths
      - name: mmenu-admin
        port: 3001
```
	
and run `kubectl apply -f /path/to/gateway.yaml`, to delete `kubectl delete -f /path/to/gateway.yaml`
	-  using container-native ingress
		- create classical ALB for each service
		- only supports classic certificate (only 1 domain, no wildcard)
		- edit `ingress.yaml` and set `ingress.enabled=true` in `values.yaml`
```yaml
{{- if .Values.ingress.enabled -}}
{{- $fullName := include "mmenu-api.fullname" . -}}
{{- $svcPort := .Values.service.port -}}
{{- if and .Values.ingress.className (not (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion)) }}
  {{- if not (hasKey .Values.ingress.annotations "kubernetes.io/ingress.class") }}
  {{- $_ := set .Values.ingress.annotations "kubernetes.io/ingress.class" .Values.ingress.className}}
  {{- end }}
{{- end }}
{{- if semverCompare ">=1.19-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1
{{- else if semverCompare ">=1.14-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1beta1
{{- else -}}
apiVersion: extensions/v1beta1
{{- end }}
kind: Ingress
metadata:
  name: {{ $fullName }}
  labels:
    {{- include "mmenu-api.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  # add defaultBackend for container-native ingress
  defaultBackend:
    service:
	  name: {{ include "mmenu-api.fullname" . }}
      port:
        number: {{ .Values.service.port }}
  {{- if and .Values.ingress.className (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion) }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            {{- if and .pathType (semverCompare ">=2.18-0" $.Capabilities.KubeVersion.GitVersion) }}
            pathType: {{ .pathType }}
            {{- end }}
            backend:
              {{- if semverCompare ">=1.19-0" $.Capabilities.KubeVersion.GitVersion }}
              service:
                name: {{ $fullName }}
                port:
                  number: {{ $svcPort }}
              {{- else }}
              serviceName: {{ $fullName }}
              servicePort: {{ $svcPort }}
              {{- end }}
          {{- end }}
    {{- end }}
{{- end }}

```
- install or upgrade deployment with `helm install` or `helm upgrade --install`
```bash
helm upgrade --install mmenu-api ./mmenu-api --namespace mmenu-prod --set image.repository=asia-southeast1-docker.pkg.dev`/mmenu-api-prod/docker/mmenu-api --set image.tag=latest
```
 - better way to update a running deployment
```bash
kubectl set image deployment/<deployment-name> -n <namespace> <deployment-name>=<image>:<tag>  # changed by tag
```
1. add **A record** to DNS for gateway load balancer's ip address (if using gateway) or ingress load balancer's ip address (if using ingress)
2. Some useful kubectl commands
	see more at [kubectl cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)