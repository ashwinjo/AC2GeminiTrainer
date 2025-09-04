# R01: OTG Glossary

## 📚 Overview
This comprehensive glossary defines key terms, concepts, and acronyms used throughout the OTG ecosystem. Use this as a quick reference while working through labs and documentation.

---

## A

### **API (Application Programming Interface)**
A set of protocols and tools for building software applications. In OTG context, refers to the REST API used to control traffic generators.

### **ARP (Address Resolution Protocol)**
Protocol used to discover the link layer address (MAC address) associated with a given network layer address (IP address).

### **AS (Autonomous System)**
A collection of connected Internet Protocol (IP) routing prefixes under the control of one or more network operators.

### **Async/Asynchronous**
Programming pattern where operations can run concurrently without blocking the main execution thread.

---

## B

### **BGP (Border Gateway Protocol)**
Standardized exterior gateway protocol designed to exchange routing information between autonomous systems on the Internet.

### **Back-to-Back (B2B) Testing**
Network testing methodology where two devices are directly connected without intermediate network equipment.

### **BPS (Bits Per Second)**
Unit of measurement for data transfer rate, indicating how many bits are transmitted per second.

### **Burst**
A temporary increase in traffic rate above the configured sustained rate.

---

## C

### **Container**
Lightweight, standalone package that includes everything needed to run an application: code, runtime, system tools, libraries, and settings.

### **Control Plane**
Part of a network that carries signaling traffic and is responsible for routing decisions.

### **CPS (Connections Per Second)**
Measurement of how many new connections can be established per second.

---

## D

### **Data Plane**
Part of a network that carries user traffic and forwards packets based on control plane decisions.

### **DDoS (Distributed Denial of Service)**
Attack where multiple compromised systems are used to target a single system, causing denial of service.

### **DPDK (Data Plane Development Kit)**
Set of libraries and drivers for fast packet processing on x86 platforms.

### **DUT (Device Under Test)**
The network device or system being tested in a laboratory environment.

---

## E

### **Endpoint**
A device or node that serves as a source or destination for network traffic.

### **Ethernet**
Family of computer networking technologies commonly used in local area networks (LANs).

---

## F

### **Flow**
A stream of packets sharing common characteristics, typically defined by source/destination addresses and ports.

### **FPS (Frames Per Second)**
Number of data frames transmitted per second, commonly used in network performance measurement.

---

## G

### **gNMI (gRPC Network Management Interface)**
Network management protocol that uses gRPC for configuration and telemetry collection.

### **gRPC (gRPC Remote Procedure Call)**
High-performance, open-source RPC framework that can run in any environment.

---

## H

### **HTTP/HTTPS (HyperText Transfer Protocol/Secure)**
Application protocol for distributed, collaborative, hypermedia information systems. HTTPS is the secure version.

---

## I

### **IETF (Internet Engineering Task Force)**
Standards organization for the Internet, responsible for developing and promoting Internet standards.

### **IP (Internet Protocol)**
Network layer protocol that provides addressing and routing functions for data packets.

### **IPAM (IP Address Management)**
Planning, tracking, and managing IP address space used in a network.

### **Ixia-c**
Keysight's containerized traffic generator implementation based on OTG specifications.

---

## J

### **Jitter**
Variation in packet delay, measured as the difference in packet arrival times.

### **JSON (JavaScript Object Notation)**
Lightweight data-interchange format that is easy for humans to read and write.

---

## K

### **KENG (Keysight Elastic Network Generator)**
Keysight's cloud-native implementation of the Open Traffic Generator specification.

### **Kubernetes (K8s)**
Open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.

---

## L

### **L2/L3/L4/L7**
References to different layers of the OSI model:
- **L2**: Data Link Layer (Ethernet, MAC addresses)
- **L3**: Network Layer (IP, routing)
- **L4**: Transport Layer (TCP, UDP)
- **L7**: Application Layer (HTTP, FTP, etc.)

### **Latency**
Time delay between the transmission of a packet and its receipt at the destination.

### **Load Balancer**
Device that distributes network traffic across multiple servers to ensure no single server bears too much demand.

---

## M

### **MAC (Media Access Control) Address**
Unique identifier assigned to network interfaces for communications at the data link layer.

### **MTU (Maximum Transmission Unit)**
Largest size packet that can be transmitted over a network interface.

### **Multicast**
Communication where data is addressed to a group of destination computers simultaneously.

---

## N

### **NAT (Network Address Translation)**
Method of mapping an IP address space into another by modifying network address information.

### **NIC (Network Interface Card)**
Hardware component that connects a computer to a network.

---

## O

### **OpenAPI**
Specification for describing REST APIs, formerly known as Swagger.

### **OTG (Open Traffic Generator)**
Vendor-neutral, open-source approach to network traffic generation and testing.

---

## P

### **Packet**
Formatted unit of data carried by a packet-switched network.

### **Packet Loss**
Failure of one or more transmitted packets to arrive at their destination.

### **PDU (Protocol Data Unit)**
Information that is delivered as a unit among peer entities of a network.

### **PPS (Packets Per Second)**
Measurement of packet transmission rate.

### **Protocol Stack**
Set of network protocols that work together to provide networking functionality.

---

## Q

### **QoS (Quality of Service)**
Mechanism to control and manage network resources by providing different priority to different applications or data flows.

---

## R

### **REST (Representational State Transfer)**
Architectural style for designing networked applications, commonly used for web APIs.

### **RFC (Request for Comments)**
Publication series from the IETF that describes methods, behaviors, research, or innovations applicable to the Internet.

### **RPC (Remote Procedure Call)**
Protocol that allows a program to execute a procedure on another computer as if it were a local procedure call.

### **RTT (Round Trip Time)**
Time it takes for a signal to travel from sender to receiver and back again.

---

## S

### **SDN (Software-Defined Networking)**
Approach to network management that enables dynamic, programmatically efficient network configuration.

### **SLA (Service Level Agreement)**
Commitment between a service provider and client defining the level of service expected.

### **SNMP (Simple Network Management Protocol)**
Internet standard protocol for collecting and organizing information about managed devices on IP networks.

---

## T

### **TCP (Transmission Control Protocol)**
Connection-oriented protocol that provides reliable, ordered delivery of data between applications.

### **Telemetry**
Automatic recording and transmission of data from remote sources.

### **Throughput**
Rate of successful message delivery over a communication channel.

### **TLS (Transport Layer Security)**
Cryptographic protocol that provides communications security over a computer network.

---

## U

### **UDP (User Datagram Protocol)**
Connectionless protocol that provides a simple interface between applications and the network layer.

### **Unicast**
Communication where information is sent from one sender to one receiver.

---

## V

### **VLAN (Virtual Local Area Network)**
Method of creating logically separate networks within the same physical network infrastructure.

### **VNF (Virtual Network Function)**
Software implementation of a network function that can be deployed on virtual machines or containers.

### **VPN (Virtual Private Network)**
Extends a private network across a public network, enabling secure communication.

---

## W

### **WebSocket**
Communication protocol that provides full-duplex communication channels over a single TCP connection.

---

## Y

### **YAML (YAML Ain't Markup Language)**
Human-readable data serialization standard commonly used for configuration files.

---

## 🔧 OTG-Specific Terms

### **Configuration Model**
JSON/YAML structure that defines the complete test setup including devices, ports, flows, and protocols.

### **Device**
Logical representation of a network endpoint (router, switch, server) in OTG configuration.

### **Flow Metrics**
Statistics collected for individual traffic flows, including packet counts, byte counts, and performance metrics.

### **Port**
Network interface on a device, can be physical or virtual.

### **Protocol Engine**
Software component responsible for implementing network protocol stacks and state machines.

### **Traffic Engine**
High-performance component responsible for packet generation and processing.

---

## 🏗️ Container and Cloud Terms

### **Docker**
Platform for developing, shipping, and running applications in containers.

### **Docker Compose**
Tool for defining and running multi-container Docker applications.

### **Dockerfile**
Text file containing instructions for building a Docker image.

### **Image**
Read-only template used to create containers.

### **Microservices**
Architectural style that structures an application as a collection of loosely coupled services.

### **Orchestration**
Automated configuration, coordination, and management of computer systems and services.

---

## 📊 Performance and Testing Terms

### **Baseline**
Initial measurement or configuration used as a reference point for comparison.

### **Benchmark**
Standard test used to evaluate and compare performance.

### **Load Testing**
Testing performed to understand the behavior of a system under expected load conditions.

### **Regression Testing**
Testing to ensure that previously developed and tested software still performs correctly after changes.

### **Stress Testing**
Testing performed to determine system behavior under extreme load conditions.

---

## 🔍 Measurement and Analysis Terms

### **Counter**
Numeric value that tracks occurrences of specific events (packets transmitted, errors, etc.).

### **Gauge**
Metric that represents a single numerical value that can go up or down.

### **Histogram**
Statistical distribution of values over time, showing frequency of occurrence.

### **Percentile**
Value below which a certain percentage of observations fall (e.g., 95th percentile latency).

### **Time Series**
Sequence of data points indexed by time, used for monitoring and analysis.

---

## 🛠️ Development and Integration Terms

### **CI/CD (Continuous Integration/Continuous Deployment)**
Software development practices involving frequent integration and automated deployment.

### **Git**
Distributed version control system for tracking changes in source code.

### **IDE (Integrated Development Environment)**
Software application providing comprehensive facilities for software development.

### **SDK (Software Development Kit)**
Collection of software development tools for creating applications.

### **Virtual Environment**
Isolated Python environment that allows packages to be installed for use by a particular application.

---

## 📖 Usage Examples

### Common Command Patterns
```bash
# OTG API calls
GET /config          # Retrieve current configuration
POST /config         # Apply new configuration  
POST /control/start  # Start traffic
GET /results/metrics # Get statistics

# Docker commands
docker run           # Start container
docker ps           # List containers
docker logs         # View container logs
docker stop         # Stop container
```

### Configuration Examples
```yaml
# Basic flow configuration
flows:
  - name: "test_flow"
    tx:
      device: "tx_device"
      port: "tx_port"
    rx:
      device: "rx_device" 
      port: "rx_port"
    rate:
      pps: 1000
    size:
      fixed: 64
```

---

## 🎯 Quick Reference Categories

### **Performance Metrics**
- **Throughput**: Data transfer rate
- **Latency**: End-to-end delay
- **Jitter**: Delay variation
- **Loss**: Packet loss percentage
- **Utilization**: Resource usage percentage

### **Traffic Patterns**
- **Constant**: Fixed rate traffic
- **Burst**: Periodic high-rate traffic
- **Ramp**: Gradually increasing/decreasing rate
- **Random**: Variable rate traffic

### **Test Types**
- **Functional**: Feature validation
- **Performance**: Speed and capacity testing
- **Stress**: Breaking point analysis
- **Regression**: Change validation
- **Conformance**: Standards compliance

---

**💡 Pro Tip**: Bookmark this glossary and use Ctrl+F (Cmd+F on Mac) to quickly find definitions while working through labs and documentation!

This glossary is continuously updated. If you encounter terms not defined here, please contribute by suggesting additions! 🌟
