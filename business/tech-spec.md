```markdown
# Technical Specification for mesh-vlan

## Stack
- **Language**: Go (for backend services)
- **Framework**: Gin (for HTTP server)
- **Runtime**: Docker containers orchestrated by Kubernetes
- **Frontend**: React.js with TypeScript
- **Database**: PostgreSQL (for relational data)
- **Message Queue**: RabbitMQ (for asynchronous processing)
- **Mesh Networking**: OpenWRT (for Wi-Fi mesh capabilities)

## Hosting
- **Free-Tier-First Platforms**:
  - **Google Cloud Platform (GCP)**: Free tier for Compute Engine, Cloud SQL, and Cloud Pub/Sub.
  - **AWS**: Free tier for EC2, RDS, and SQS.
  - **DigitalOcean**: Free tier for Droplets and Managed Databases.
- **Specific Platforms**:
  - **Kubernetes**: Managed Kubernetes services like GKE, EKS, or AKS.
  - **CI/CD**: GitHub Actions for continuous integration and deployment.

## Data Model
### Tables/Collections
1. **SSIDs**
   - `id` (UUID)
   - `name` (String)
   - `vlan_id` (Integer)
   - `encryption_type` (String)
   - `password` (String, encrypted)

2. **AccessPoints**
   - `id` (UUID)
   - `name` (String)
   - `ip_address` (String)
   - `mac_address` (String)
   - `status` (String)

3. **MeshNodes**
   - `id` (UUID)
   - `name` (String)
   - `ip_address` (String)
   - `mac_address` (String)
   - `parent_node_id` (UUID, nullable)

4. **Users**
   - `id` (UUID)
   - `username` (String)
   - `email` (String)
   - `password_hash` (String)
   - `role` (String)

## API Surface
1. **GET /api/ssids**
   - Purpose: Retrieve a list of all SSIDs.

2. **POST /api/ssids**
   - Purpose: Create a new SSID.

3. **GET /api/ssids/{id}**
   - Purpose: Retrieve details of a specific SSID.

4. **PUT /api/ssids/{id}**
   - Purpose: Update an existing SSID.

5. **DELETE /api/ssids/{id}**
   - Purpose: Delete an SSID.

6. **GET /api/accesspoints**
   - Purpose: Retrieve a list of all access points.

7. **POST /api/accesspoints**
   - Purpose: Add a new access point.

8. **GET /api/meshnodes**
   - Purpose: Retrieve a list of all mesh nodes.

9. **POST /api/meshnodes**
   - Purpose: Add a new mesh node.

10. **GET /api/users**
    - Purpose: Retrieve a list of all users.

## Security Model
- **Authentication**: JWT (JSON Web Tokens) for API authentication.
- **Secrets**: Use environment variables for sensitive data like database credentials and API keys.
- **IAM**: Role-based access control (RBAC) for different user roles (admin, user, guest).

## Observability
- **Logs**: Centralized logging using ELK Stack (Elasticsearch, Logstash, Kibana).
- **Metrics**: Prometheus for monitoring and Grafana for visualization.
- **Traces**: Jaeger for distributed tracing.

## Build/CI
- **CI Pipeline**: GitHub Actions for automated testing and building.
- **CD Pipeline**: ArgoCD for continuous deployment to Kubernetes clusters.
- **Testing**: Unit tests, integration tests, and end-to-end tests using Jest and Cypress.
```