# Markus Bike Shop Configurator

## Project Description:

This project delivers a custom bike configuration system designed to provide a clear and simple User Experience (UX). The key features include real-time price calculation and the dynamic presentation of only compatible components, ensuring the customer's selection always results in a valid product. The price logic is implemented and validated on both the client and server sides. 

## Goals and Features

The primary goal was to create a robust and simple MVP product to allow the configuration of a customer's dream bike efficiently.

Requirement | Description

**Guided Configuration** | Stepper/Tab-based workflow (Frame $\rightarrow$ Wheels $\rightarrow$ Chain $\rightarrow$ Review and Confirm) with sequential navigation.

**Rule Validation** - **Bidirectional** |  To manage "requires" and "prohibits" rules (e.g., Mountain Wheels require Full-Suspension Frame), the system uses Bidirectional Exclusions: 1. Forward Check: Ensures that the new component is not excluded by any of the previously selected parts. 2. Backward Check: Confirms that selecting the new component does not invalidate any previously selected component.

**Dynamic Pricing** | Real-time price calculation, handling conditional pricing rules.

**Security** | Final price validation performed on the backend server to prevent client-side manipulation.

**Scalable Architecture** | Decoupled Backend and Frontend, ready for future extensions.

## Technical Architecture

The project is built on an **API-first** architecture, following **SOLID** principles.

### Frontend

  * **Framework:** **Vue 3** (Composition API)
  * **State Management:** Pinia
  * **Language:** TypeScript
  * **Key Pattern:** Reactive filtering of components using Pinia getters to maintain UI validity.

### Backend

  * **Framework:** **FastAPI** (Python)
  * **Design:** Dependency Injection (`Depends`) for testability and resource management.
  * **Core Logic:** Implements the business logic for Compatibility Validation and Final Price Calculation using the dedicated `PricingRuleApplicator` service.

## Key Design Decisions

The limited time required focusing on logical robustness and code clarity over extensive UI polish.
This ensures the resulting configuration is always valid. The user experience is enhanced by **hiding** incompatible options via the `filteredCatalogue` getter.

### Dynamic Price Calculation and Validation

The price calculation logic is implemented in two places for different purposes:

1.  **Frontend (UX):** The **`getComponentPrice`** Pinia getter provides instantaneous price updates based on current selections.
2.  **Backend (Security):** The **`PricingRuleApplicator`** class in Python performs the final price calculation considering all pricing and compatibility rules, serving as a server-side validation check upon order confirmation.

### API Data Adapter

The API endpoint (`/price/check`) acts as an **Adapter** to bridge the data format gap between the client and the business service. It converts the list of IDs received from the client into the `{category: id}` dictionary format expected by the `BikeConfiguratorService`, ensuring the business logic remains clean and consistent.

## Local Setup and Startup

### Prerequisites

  * Node.js v22.21.1 (for Frontend)
  * Python 3.12+ (for Backend)

### Instructions

1.  **Clone Repository:**
    ```bash
    git clone https://github.com/ManueleVolponi/bike-shop.git
    cd bike-shop
    ```

2.  **Start Backend:**

    ```bash
    cd path/to/your/project/server
    # Create virtual environment
    python -m venv venv

    # Activate virtual environment
    source venv/bin/activate
    # Install dependencies
    pip install -r requirements.txt

    # Create .env from .env.example
    cp -r .env.example .env
    
    fastapi dev main.py
    ```

3.  **Start Frontend:**

    ```bash
    cd path/to/your/project/client

    # Install dependencies
    npm install

    # Create .env from .env.example
    cp -r .env.example .env

    npm run dev
    ```

4. **Backend tests:**
    ```bash
    cd path/to/your/project # -> From directory path
    python -m unittest discover server
    ```

## Future Improvements

  * **Data Persistence:** Migrate configuration data, rules, and components from static files/mock gateways to a production database (e.g., PostgreSQL).
  * **Admin Interface:** Develop a dedicated CRUD interface to manage `constraints` and `pricingRules` without code deployment.
  * **Customer Portal:** Develop a dedicated CRUD interface to manage customer account and history orders.
  * **Inventory Management:** Integrate stock levels into the `CatalogueGateway` and disable components with zero availability on the frontend.
  * **Dynamic Object creation:** Allow the creation of objects like payment strategy, leveraging a Factory/Abstract Factory pattern similar to the `BikeComponent` logic.
  * **Cache implementation:** Implement cache layers to avoid always hitting the Database and improving read performance.
  * **Order Microservices:** Order Microservices: Develop dedicated microservices to manage order processing, shipping, email notifications, payments, etc.. .