---
title: "What is KENG (Keysight Elastic Network Generator)?"
concept_id: "C02"
category: "concepts"
objective: "Learn about KENG - Keysight's cloud-native implementation of OTG, its architecture, deployment models, and enterprise features."
tags: ["keng", "keysight", "cloud-native", "containers", "enterprise"]
difficulty: "intermediate"
---

# C02: What is KENG (Keysight Elastic Network Generator)?

## 🚀 Introduction
KENG (Keysight Elastic Network Generator) is Keysight's modern, cloud-native implementation of the Open Traffic Generator (OTG) specification. It represents Keysight's evolution from traditional hardware-based traffic generators to a software-defined, container-based approach.

## 🎯 KENG in the OTG Ecosystem

### Relationship to OTG
```
OTG Specification (Open Standard)
         ↓
KENG (Keysight's Implementation)
         ↓
Ixia-c (Container Platform)
         ↓
Your Network Tests
```

**KENG is to OTG what Chrome is to HTML** - a specific implementation of an open standard.

## 🏗️ Architecture Overview

### Traditional Keysight vs. KENG

**Traditional IxNetwork:**
```
[IxNetwork GUI] → [IxOS] → [Physical Chassis] → [Test Ports]
     ↓
[High Performance] + [Hardware Dependency] + [High Cost]
```

**KENG Architecture:**
```
[OTG API] → [KENG Controller] → [Ixia-c Containers] → [Virtual/Physical Ports]
     ↓
[Cloud Native] + [Software Defined] + [Cost Effective]
```

### Core Components

1. **KENG Controller**: Orchestrates test execution and resource management
2. **Ixia-c Protocol Engine**: Handles packet generation and protocol emulation
3. **Traffic Engine**: High-performance packet processing
4. **gNMI Interface**: Network management and telemetry
5. **Statistics Engine**: Real-time metrics collection and reporting

## 🌟 Key Features

### 1. Cloud-Native Design
- **Containerized**: Runs in Docker/Kubernetes environments
- **Elastic Scaling**: Scale up/down based on demand
- **Multi-Tenant**: Isolate different test environments
- **Resource Efficiency**: Optimal resource utilization

### 2. OTG Compliance
- **Standard API**: Full OTG REST API implementation
- **Interoperability**: Works with any OTG client
- **Future-Proof**: Stays current with OTG evolution
- **Vendor Neutral**: No lock-in to Keysight ecosystem

### 3. High Performance
- **DPDK Integration**: Data Plane Development Kit for speed
- **Multi-Core Support**: Leverages modern CPU architectures
- **Hardware Acceleration**: GPU and FPGA support where available
- **Optimized Networking**: Efficient packet processing pipelines

### 4. Enterprise Features
- **Security**: Enterprise-grade authentication and authorization
- **Scalability**: Supports large-scale deployments
- **Reliability**: High availability and fault tolerance
- **Support**: Professional support from Keysight

## 🔧 KENG Components Deep Dive

### KENG Controller
```yaml
# KENG Controller Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: keng-controller-config
data:
  config.yaml: |
    api:
      port: 8080
      tls: false
    licensing:
      server: "license.keysight.com"
    resources:
      max_ports: 100
      max_flows: 10000
```

**Responsibilities:**
- API endpoint management
- Resource allocation and scheduling
- License management
- Configuration validation
- Statistics aggregation

### Ixia-c Protocol Engine
```yaml
# Protocol Engine Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ixia-c-protocol-engine
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: protocol-engine
        image: ixiacom/ixia-c-protocol-engine:latest
        resources:
          limits:
            cpu: "2"
            memory: "4Gi"
          requests:
            cpu: "1"
            memory: "2Gi"
```

**Capabilities:**
- Protocol stack implementation (L2-L7)
- Packet crafting and parsing
- Protocol state machines
- Advanced protocol features

### Traffic Engine
```yaml
# Traffic Engine Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: traffic-engine-config
data:
  engine.conf: |
    [traffic]
    mode = dpdk
    cores = 4
    memory = 2048
    
    [performance]
    max_pps = 100000000
    max_flows = 1000000
```

**Features:**
- High-speed packet generation
- Line-rate traffic processing
- Precise timing control
- Hardware timestamping

## 🚀 Deployment Models

### 1. Local Development
```bash
# Quick start with Docker Compose
version: '3.8'
services:
  keng-controller:
    image: keysight/keng-controller:latest
    ports:
      - "8080:8080"
    environment:
      - LICENSE_SERVER=flex@license.company.com
  
  ixia-c-protocol-engine:
    image: ixiacom/ixia-c-protocol-engine:latest
    cap_add:
      - NET_ADMIN
    network_mode: host
```

### 2. Kubernetes Deployment
```yaml
# KENG Kubernetes Deployment
apiVersion: v1
kind: Namespace
metadata:
  name: keng-system
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: keng-controller
  namespace: keng-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: keng-controller
  template:
    metadata:
      labels:
        app: keng-controller
    spec:
      containers:
      - name: controller
        image: keysight/keng-controller:latest
        ports:
        - containerPort: 8080
        env:
        - name: KENG_LICENSE_SERVER
          value: "flex@license.company.com"
---
apiVersion: v1
kind: Service
metadata:
  name: keng-controller-service
  namespace: keng-system
spec:
  selector:
    app: keng-controller
  ports:
  - port: 8080
    targetPort: 8080
  type: LoadBalancer
```

### 3. Cloud Deployment
```terraform
# AWS EKS with KENG
resource "aws_eks_cluster" "keng_cluster" {
  name     = "keng-testing-cluster"
  role_arn = aws_iam_role.cluster.arn
  version  = "1.24"

  vpc_config {
    subnet_ids = aws_subnet.cluster[*].id
  }
}

resource "kubernetes_deployment" "keng_controller" {
  metadata {
    name      = "keng-controller"
    namespace = "keng-system"
  }

  spec {
    replicas = 3
    
    selector {
      match_labels = {
        app = "keng-controller"
      }
    }

    template {
      metadata {
        labels = {
          app = "keng-controller"
        }
      }

      spec {
        container {
          image = "keysight/keng-controller:latest"
          name  = "controller"
          
          port {
            container_port = 8080
          }
          
          resources {
            limits = {
              cpu    = "2"
              memory = "4Gi"
            }
            requests = {
              cpu    = "1"
              memory = "2Gi"
            }
          }
        }
      }
    }
  }
}
```

## 📊 Performance Characteristics

### Throughput Capabilities
| Deployment Type | Max Throughput | Typical Use Case |
|----------------|----------------|------------------|
| **Single Container** | 1-10 Gbps | Development, Small Tests |
| **Multi-Container** | 10-100 Gbps | Production Testing |
| **Kubernetes Cluster** | 100+ Gbps | Large-Scale Validation |
| **Bare Metal + DPDK** | 400+ Gbps | High-Performance Testing |

### Resource Requirements
```yaml
# Resource Planning Guide
Small Deployment (Development):
  CPU: 2-4 cores
  Memory: 4-8 GB
  Network: 1-10 Gbps

Medium Deployment (Testing):
  CPU: 8-16 cores
  Memory: 16-32 GB
  Network: 10-100 Gbps

Large Deployment (Production):
  CPU: 32+ cores
  Memory: 64+ GB
  Network: 100+ Gbps
```

## 🔧 Configuration and Management

### 1. Basic Configuration
```python
from keng_client import KengClient

# Connect to KENG controller
client = KengClient("https://keng.company.com:8080")

# Configure basic test
config = {
    "devices": [
        {
            "name": "tx_device",
            "ports": [{"name": "tx_port", "location": "eth0"}]
        }
    ],
    "flows": [
        {
            "name": "test_flow",
            "tx": {"device": "tx_device", "port": "tx_port"},
            "rate": {"gbps": 1},
            "size": {"fixed": 1518}
        }
    ]
}

client.set_config(config)
```

### 2. Advanced Protocol Configuration
```python
# BGP Route Advertisement Test
bgp_config = {
    "devices": [
        {
            "name": "bgp_speaker",
            "bgp": {
                "router_id": "1.1.1.1",
                "as_number": 65001,
                "peers": [
                    {
                        "name": "peer1",
                        "peer_address": "192.168.1.2",
                        "as_number": 65002,
                        "routes": {
                            "ipv4": [
                                {
                                    "prefix": "10.0.0.0/8",
                                    "count": 10000,
                                    "step": 256
                                }
                            ]
                        }
                    }
                ]
            }
        }
    ]
}
```

### 3. Monitoring and Observability
```python
# Real-time metrics collection
import asyncio

async def monitor_test():
    while True:
        metrics = await client.get_metrics()
        
        print(f"Throughput: {metrics['throughput_gbps']:.2f} Gbps")
        print(f"Packet Loss: {metrics['loss_percent']:.4f}%")
        print(f"Latency: {metrics['avg_latency_us']:.1f} μs")
        
        await asyncio.sleep(1)

# Prometheus metrics export
from prometheus_client import start_http_server, Gauge

throughput_gauge = Gauge('keng_throughput_gbps', 'Current throughput in Gbps')
latency_gauge = Gauge('keng_latency_microseconds', 'Average latency in microseconds')

start_http_server(8000)
```

## 🎯 Use Cases and Applications

### 1. Network Equipment Testing
```python
# Switch validation test
def test_switch_capacity():
    config = create_mesh_traffic_config(
        ports=24,
        rate_per_port="1gbps",
        packet_sizes=[64, 128, 256, 512, 1024, 1518]
    )
    
    results = run_test_suite(config, duration="5min")
    return validate_switch_performance(results)
```

### 2. Cloud Network Validation
```python
# Kubernetes network policy testing
def test_k8s_network_policies():
    config = create_pod_to_pod_traffic(
        source_pods=["app-tier"],
        dest_pods=["db-tier"],
        expected_behavior="blocked"
    )
    
    results = run_security_test(config)
    return validate_policy_enforcement(results)
```

### 3. 5G Core Network Testing
```python
# 5G UPF (User Plane Function) testing
def test_5g_upf_performance():
    config = create_5g_traffic_config(
        subscribers=1000000,
        sessions_per_subscriber=2,
        traffic_mix={
            "http": 60,
            "video": 30,
            "gaming": 10
        }
    )
    
    return run_5g_performance_test(config)
```

## 🔒 Security and Compliance

### Authentication and Authorization
```yaml
# RBAC Configuration
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: keng-operator
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["create", "delete", "get", "list", "update"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["create", "delete", "get", "list", "update"]
```

### Network Security
```yaml
# Network Policies
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: keng-network-policy
spec:
  podSelector:
    matchLabels:
      app: keng-controller
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: keng-client
    ports:
    - protocol: TCP
      port: 8080
```

## 📈 Scaling and Performance Optimization

### Horizontal Scaling
```yaml
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: keng-controller-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: keng-controller
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Performance Tuning
```bash
# System-level optimizations
echo 'net.core.rmem_max = 268435456' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 268435456' >> /etc/sysctl.conf
echo 'net.core.netdev_max_backlog = 5000' >> /etc/sysctl.conf

# CPU isolation for DPDK
echo 'isolcpus=2-7' >> /proc/cmdline

# Huge pages configuration
echo 'vm.nr_hugepages = 1024' >> /etc/sysctl.conf
```

## 🚀 Future Roadmap

### Upcoming Features
1. **AI-Powered Test Optimization**: Machine learning for test parameter optimization
2. **Intent-Based Testing**: High-level test specification language
3. **Edge Computing Support**: Distributed testing across edge locations
4. **5G Advanced Features**: Support for latest 5G specifications

### Integration Roadmap
1. **CI/CD Platforms**: Native integrations with Jenkins, GitLab, etc.
2. **Observability Tools**: Enhanced Prometheus, Grafana integration
3. **Cloud Platforms**: Deeper integration with AWS, Azure, GCP
4. **Network Orchestration**: Integration with Kubernetes network operators

## 📚 Learning Resources

### Official Documentation
- [KENG User Guide](https://www.keysight.com/us/en/products/network-test/protocol-load-test/keysight-elastic-network-generator.html)
- [Ixia-c Documentation](https://github.com/open-traffic-generator/ixia-c)

### Training and Certification
- Keysight University courses
- OTG certification programs
- Hands-on workshops and labs

### Community Resources
- [KENG GitHub Repository](https://github.com/keysight-keng)
- User forums and discussion groups
- Regular webinars and technical sessions

---

## 🎯 Key Takeaways

1. **KENG is Keysight's OTG implementation** - Modern, cloud-native traffic generation
2. **Enterprise-grade features** - Security, scalability, and professional support
3. **Container-native architecture** - Built for modern deployment models
4. **High performance** - Leverages latest hardware and software optimizations
5. **Open ecosystem** - Based on open standards with vendor neutrality

KENG represents Keysight's commitment to the future of network testing - combining the reliability and performance of traditional Keysight solutions with the flexibility and scalability of modern cloud-native architectures! 🌟
