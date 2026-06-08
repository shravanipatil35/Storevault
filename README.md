# Storevault

Storevault is a modern, containerized inventory management system designed to streamline stock tracking and Point of Sale (POS) operations. It is built to be efficient, reliable, and scalable for production environments.

About the Application
Storevault provides a digital interface for managing inventory effectively. It includes:

User Authentication: Secure login and registration functionality to manage system access.

Inventory Management: A centralized platform to track products and stock levels.

POS Functionality: Integrated features to handle transaction processing smoothly.

Technologies Used
Backend: Developed using Python with the Flask web framework, known for its lightweight and flexible structure.

Data Handling: Uses PostgreSQL (via psycopg2-binary) for robust, relational database management.

Frontend: Built with HTML and CSS for an intuitive user interface.

Infrastructure as Code: Uses HCL (HashiCorp Configuration Language) via Terraform to manage infrastructure.

Cloud & DevOps: Key Components
Your deployment leverages a professional-grade cloud architecture on AWS, specifically utilizing Amazon EKS (Elastic Kubernetes Service) to orchestrate containers.

Orchestration: Kubernetes ensures your application is self-healing, scalable, and highly available across multiple nodes.

Networking/Traffic Management: * AWS ALB (Application Load Balancer): Automatically routes incoming internet traffic to your application pods.

Ingress Controller: Manages external access to the services within the cluster, configured with specific health checks and success codes.

Containerization: Docker is used to package the application, ensuring consistency across development, testing, and production environments.

Automation:

Terraform: Automates the provisioning of your EKS cluster and networking infrastructure.

CI/CD Pipeline: Integrated workflows to streamline building, testing, and deploying images to your Kubernetes cluster.
