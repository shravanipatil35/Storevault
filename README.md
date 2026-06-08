# StoreVault

StoreVault is a modern, containerized inventory management system designed to streamline stock tracking and Point of Sale (POS) operations. It is built to be efficient, reliable, and scalable for production environments.

---

### 📱 About the Application
StoreVault provides a digital interface for managing inventory effectively. Key features include:

* **User Authentication:** Secure login and registration functionality to manage system access.
* **Inventory Management:** A centralized platform to track products and stock levels.
* **POS Functionality:** Integrated features to handle transaction processing smoothly.

---

### 🛠 Technologies Used
* **Backend:** Developed using **Python** with the **Flask** web framework.
* **Data Handling:** Uses **PostgreSQL** (via `psycopg2-binary`) for robust, relational database management.
* **Frontend:** Built with **HTML** and **CSS** for an intuitive user interface.
* **Infrastructure as Code:** Uses **HCL** (HashiCorp Configuration Language) via **Terraform** to manage infrastructure.

---

### ☁️ Cloud & DevOps Key Components
The deployment leverages a professional-grade cloud architecture on **AWS**, specifically utilizing **Amazon EKS (Elastic Kubernetes Service)** to orchestrate containers.

| Component | Description |
| :--- | :--- |
| **Orchestration** | **Kubernetes** ensures your application is self-healing, scalable, and highly available. |
| **Traffic Management** | **AWS ALB (Application Load Balancer)** routes incoming internet traffic to application pods. |
| **Ingress Control** | Manages external access, configured with specific health checks and success codes. |
| **Containerization** | **Docker** packages the application for consistency across all environments. |
| **Automation** | **Terraform** automates the provisioning of the EKS cluster and networking. |
| **CI/CD Pipeline** | Integrated workflows streamline building, testing, and deploying to the cluster. |
