package main

# Kubernetes Security Policy
# Open Policy Agent (OPA) / Conftest policy for Kubernetes manifest validation
# OPA Rego v1 syntax (OPA 0.50+)

import rego.v1

# Deny if container doesn't set runAsNonRoot
deny contains msg if {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.securityContext.runAsNonRoot
  msg := sprintf("Container '%s' does not set securityContext.runAsNonRoot", [container.name])
}

# Deny if container doesn't set allowPrivilegeEscalation to false
deny contains msg if {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.securityContext.allowPrivilegeEscalation == false
  msg := sprintf("Container '%s' does not set securityContext.allowPrivilegeEscalation=false", [container.name])
}

# Deny if container runs as privileged
deny contains msg if {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  container.securityContext.privileged == true
  msg := sprintf("Container '%s' runs as privileged (very dangerous)", [container.name])
}

# Deny if container uses 'latest' tag
deny contains msg if {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  endswith(container.image, ":latest")
  msg := sprintf("Container '%s' uses 'latest' tag (non-deterministic)", [container.name])
}

# Warn if no resource limits defined
warn contains msg if {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.resources.limits
  msg := sprintf("Container '%s' has no resource limits defined (could impact cluster stability)", [container.name])
}

# Warn if no resource requests defined
warn contains msg if {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.resources.requests
  msg := sprintf("Container '%s' has no resource requests defined", [container.name])
}

# Deny if Service uses LoadBalancer type (public exposure)
deny contains msg if {
  input.kind == "Service"
  input.spec.type == "LoadBalancer"
  msg := "Service uses LoadBalancer type (exposes publicly, consider NodePort or ClusterIP)"
}

# Warn if no liveness probe defined
warn contains msg if {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.livenessProbe
  msg := sprintf("Container '%s' has no livenessProbe defined", [container.name])
}

# Warn if no readiness probe defined
warn contains msg if {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.readinessProbe
  msg := sprintf("Container '%s' has no readinessProbe defined", [container.name])
}

# Deny if container has dangerous capabilities
deny contains msg if {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  container.securityContext.capabilities.add[_] == "SYS_ADMIN"
  msg := sprintf("Container '%s' requests SYS_ADMIN capability (dangerous)", [container.name])
}

# Deny if readOnlyRootFilesystem is not set to true
warn contains msg if {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.securityContext.readOnlyRootFilesystem == true
  msg := sprintf("Container '%s' does not set securityContext.readOnlyRootFilesystem=true", [container.name])
}
