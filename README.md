# 🍱 RescueLink

### Serverless Food Redistribution Platform

RescueLink is a serverless AWS platform designed to connect food donors
with charities, volunteers, and receivers to help reduce food waste and
redistribute surplus food.

The application provides secure role-based access for **DONOR**,
**RECEIVER**, and **ADMIN** users and uses AWS services for
authentication, APIs, database management, notifications, automation,
monitoring, reporting, and location services.

------------------------------------------------------------------------

## 📌 Table of Contents

-   [Overview](#-overview)
-   [Problem Statement](#-problem-statement)
-   [Solution](#-solution)
-   [Key Features](#-key-features)
-   [User Roles](#-user-roles)
-   [Donation Workflow](#-donation-workflow)
-   [Architecture](#️-architecture)
-   [AWS Services](#️-aws-services)
-   [Application Flow](#-application-flow)
-   [Database Design](#️-database-design)
-   [Authentication and
    Authorization](#-authentication-and-authorization)
-   [API Endpoints](#-api-endpoints)
-   [Event-Driven Architecture](#-event-driven-architecture)
-   [Notifications](#-notifications)
-   [Automatic Donation Expiry](#️-automatic-donation-expiry)
-   [Location Services](#️-location-services)
-   [Admin Dashboard](#-admin-dashboard)
-   [Reporting](#-reporting)
-   [CSV Export](#-csv-export)
-   [Security](#-security)
-   [Monitoring](#-monitoring)
-   [Technology Stack](#️-technology-stack)
-   [Project Structure](#-project-structure)
-   [Local Setup](#-local-setup)
-   [Configuration](#-configuration)
-   [AWS Regions](#-aws-regions)
-   [Testing](#-testing)
-   [Future Improvements](#-future-improvements)
-   [Learning Outcomes](#-learning-outcomes)
-   [Resume Description](#-resume-description)
-   [Portfolio Description](#-portfolio-description)
-   [Author](#-author)
-   [License](#-license)

------------------------------------------------------------------------

# 📖 Overview

Food waste is a major environmental and social problem. At the same
time, charities and communities may need access to food resources.

RescueLink provides a digital platform where food donors can publish
surplus food donations and receivers can discover, claim, collect, and
complete those donations.

The project demonstrates how a real-world application can be built using
a **serverless AWS architecture** without maintaining traditional
application servers.

------------------------------------------------------------------------

# 🎯 Problem Statement

Restaurants, grocery stores, and other food providers may have surplus
food that is still usable but cannot be sold.

At the same time:

-   Charities may need food donations.
-   Volunteers may be available for pickup.
-   Donors need a simple way to publish surplus food.
-   Receivers need a way to discover and claim donations.
-   Administrators need visibility into donation activity.
-   Donation availability can change quickly.

RescueLink provides a centralized workflow for managing these
activities.

------------------------------------------------------------------------

# 💡 Solution

The basic workflow is:

``` text
Food Donor
    │
    │ Creates donation
    ▼
RescueLink
    │
    │ Donation becomes available
    ▼
Receiver
    │
    │ Claims donation
    ▼
Pickup
    │
    ▼
Completion
```

The platform combines authentication, APIs, serverless compute, NoSQL
storage, event-driven automation, notifications, location services,
reporting, and monitoring.

------------------------------------------------------------------------

# ✨ Key Features

### 🔐 Authentication

-   Amazon Cognito authentication
-   JWT-based API authorization
-   Secure login
-   Role-based access

### 👥 Role-Based Access

-   DONOR
-   RECEIVER
-   ADMIN

### 🍱 Donation Management

Donors can:

-   Create donations
-   Specify food type
-   Specify quantity
-   Specify pickup location
-   Specify pickup time
-   Add descriptions
-   View their donations
-   Cancel eligible donations

### 🤝 Donation Claiming

Receivers can:

-   View available donations
-   Claim donations
-   View their claimed donations
-   Mark donations as picked up
-   Mark donations as completed

### ⏰ Automatic Expiry

Available donations can automatically change to `EXPIRED` after their
pickup time passes.

### 📧 Event-Driven Notifications

Notifications are triggered for important donation lifecycle events
using Amazon EventBridge and Amazon SNS.

### 📍 Location Services

Amazon Location Service provides:

-   Address search
-   Geocoding
-   Coordinate retrieval
-   Map visualization

### 📊 Admin Dashboard

Administrators can view:

-   Donation statistics
-   Users
-   Donation status breakdown
-   Food-type breakdown
-   Completion rate
-   Food portions
-   Donation records

### 📤 CSV Export

Administrators can export donation records as CSV.

### 📈 Monitoring

Amazon CloudWatch provides:

-   Lambda logs
-   API monitoring
-   Error alarms
-   Log retention

------------------------------------------------------------------------

# 👥 User Roles

## 🏪 DONOR

Represents a restaurant, grocery store, organization, or other food
provider.

### Permissions

-   Create donations
-   View own donations
-   Cancel eligible donations
-   Provide pickup details

------------------------------------------------------------------------

## 🤝 RECEIVER

Represents a charity, volunteer, organization, or other recipient.

### Permissions

-   View available donations
-   Claim donations
-   Mark donations as picked up
-   Mark donations as completed

------------------------------------------------------------------------

## 👑 ADMIN

Manages and monitors the platform.

### Permissions

-   View all donations
-   View users
-   View reports
-   View dashboard statistics
-   Export donation data
-   Manage donation statuses

------------------------------------------------------------------------

# 🔄 Donation Workflow

The primary donation lifecycle is:

``` text
┌───────────────┐
│    CREATE     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   AVAILABLE   │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    CLAIMED    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   PICKED_UP   │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   COMPLETED   │
└───────────────┘
```

Alternative states:

``` text
AVAILABLE ───────► EXPIRED

AVAILABLE ───────► CANCELLED
```

### Donation Statuses

  Status        Meaning
  ------------- -------------------------------------
  `AVAILABLE`   Donation can be claimed
  `CLAIMED`     A receiver has claimed the donation
  `PICKED_UP`   Receiver has collected the donation
  `COMPLETED`   Donation lifecycle completed
  `EXPIRED`     Pickup time has passed
  `CANCELLED`   Donation was cancelled

------------------------------------------------------------------------

# 🏗️ Architecture

``` text
                         ┌──────────────────┐
                         │      USERS       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Streamlit     │
                         │    Frontend      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Amazon Cognito   │
                         │ Authentication   │
                         └────────┬─────────┘
                                  │
                               JWT Token
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  API Gateway     │
                         │  RescueLinkAPI   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   AWS Lambda     │
                         │ Python Backend   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    DynamoDB      │
                         │   RescueLink     │
                         └──────────────────┘

       EventBridge ─────► Notification Lambda ─────► SNS ─────► Email
             │
             └──────────► Expiry Lambda

       Streamlit ───────► Amazon Location Service
```

------------------------------------------------------------------------

# ☁️ AWS Services

  AWS Service                   Purpose
  ----------------------------- ----------------------------------
  **Amazon Cognito**            Authentication and user identity
  **Amazon API Gateway**        HTTP API
  **AWS Lambda**                Serverless backend
  **Amazon DynamoDB**           NoSQL database
  **Amazon EventBridge**        Event-driven automation
  **Amazon SNS**                Email notifications
  **Amazon Location Service**   Geocoding and location services
  **Amazon CloudWatch**         Logs and monitoring
  **AWS IAM**                   Permissions and security

------------------------------------------------------------------------

# 🔁 Application Flow

## Creating a Donation

``` text
DONOR
  │
  ▼
Streamlit
  │
  ▼
Cognito JWT
  │
  ▼
API Gateway
  │
  ▼
CreateDonation Lambda
  │
  ▼
DynamoDB
  │
  ▼
Donation Created
```

## Claiming a Donation

``` text
RECEIVER
   │
   ▼
Available Donations
   │
   ▼
Claim
   │
   ▼
API Gateway
   │
   ▼
Claim Lambda
   │
   ▼
DynamoDB
   │
   ▼
AVAILABLE → CLAIMED
   │
   ▼
EventBridge
   │
   ▼
SNS Notification
```

## Completing a Donation

``` text
CLAIMED
   │
   ▼
PICKED_UP
   │
   ▼
COMPLETED
```

------------------------------------------------------------------------

# 🗄️ Database Design

RescueLink uses Amazon DynamoDB.

## Main Table

``` text
Table: RescueLink
Partition Key: PK
Sort Key: SK
```

Example donation item:

``` json
{
  "PK": "DONATION#456",
  "SK": "DETAILS",
  "donationId": "456",
  "donorId": "123",
  "foodType": "Prepared meals",
  "quantity": 25,
  "pickupLocation": "Central Market",
  "pickupTime": "2026-04-01T18:00:00Z",
  "description": "Fresh prepared meals",
  "status": "AVAILABLE",
  "claimedBy": null,
  "createdAt": "2026-04-01T12:00:00Z"
}
```

------------------------------------------------------------------------

# 👤 User Database

Application roles are stored in a separate DynamoDB table.

``` text
Table: RescueLinkUsers
Primary Key: userId
```

Example:

``` text
userId
email
role
```

Supported roles:

``` text
DONOR
RECEIVER
ADMIN
```

------------------------------------------------------------------------

# 🔐 Authentication and Authorization

RescueLink uses **Amazon Cognito** for authentication.

``` text
User
 │
 ▼
Amazon Cognito
 │
 ▼
JWT Token
 │
 ▼
API Gateway
 │
 ▼
Lambda
```

API Gateway validates the Cognito JWT using a JWT authorizer.

Lambda functions perform application-level role checks.

------------------------------------------------------------------------

# 🛡️ Role-Based Authorization

``` text
DONOR
 ├── Create Donation
 └── Cancel Eligible Donation

RECEIVER
 ├── Claim Donation
 ├── Mark Picked Up
 └── Mark Completed

ADMIN
 ├── View All Donations
 ├── View Users
 ├── View Reports
 └── Manage Donation Status
```

------------------------------------------------------------------------

# 🔌 API Endpoints

  Method    Endpoint                   Description
  --------- -------------------------- --------------------------
  `GET`     `/donations`               List available donations
  `GET`     `/donations/{id}`          Get donation details
  `POST`    `/donations`               Create donation
  `POST`    `/donations/{id}/claim`    Claim donation
  `PATCH`   `/donations/{id}/status`   Update donation status
  `GET`     `/dashboard`               Dashboard data
  `GET`     `/my-donations`            User's donations
  `GET`     `/admin/donations`         Admin donation list
  `GET`     `/admin/users`             Admin user list
  `GET`     `/admin/reports`           Admin reporting data

------------------------------------------------------------------------

# ⚡ Event-Driven Architecture

RescueLink uses Amazon EventBridge to process donation lifecycle events.

Events include:

``` text
Donation Claimed
Donation Picked Up
Donation Completed
Donation Cancelled
Donation Expired
```

The notification system is separated from the core donation API.

``` text
Donation API
     │
     ▼
EventBridge
     │
     ▼
Notification Lambda
     │
     ▼
Amazon SNS
     │
     ▼
Email
```

------------------------------------------------------------------------

# 📧 Notifications

Amazon SNS is used for email notifications.

Notification flow:

``` text
Donation Event
      │
      ▼
EventBridge
      │
      ▼
Notification Lambda
      │
      ▼
Amazon SNS
      │
      ▼
Email
```

The implemented notification workflow includes:

-   Donation Claimed
-   Donation Picked Up
-   Donation Completed

------------------------------------------------------------------------

# ⏰ Automatic Donation Expiry

An EventBridge scheduled rule periodically triggers:

``` text
RescueLink-expireDonations
```

The Lambda checks available donations and identifies donations whose
pickup time has passed.

``` text
EventBridge
     │
     ▼
Expiry Lambda
     │
     ▼
Find AVAILABLE donations
     │
     ▼
Compare pickupTime
     │
     ▼
Pickup time passed
     │
     ▼
status = EXPIRED
```

------------------------------------------------------------------------

# 📍 Amazon Location Service

Amazon Location Service is used for location functionality.

Features include:

-   Address search
-   Geocoding
-   Reverse geocoding
-   Coordinate retrieval
-   Map visualization

Example:

``` text
"Tirupati Central Market"
          │
          ▼
Amazon Location Service
          │
          ▼
Latitude / Longitude
          │
          ▼
Map
```

------------------------------------------------------------------------

# 📊 Admin Dashboard

The admin dashboard provides centralized platform statistics.

Metrics include:

``` text
Total Donations
Available Donations
Claimed Donations
Picked Up Donations
Completed Donations
Expired Donations
Cancelled Donations
Total Food Portions
Completed Food Portions
Completion Rate
Active Donors
Active Receivers
```

------------------------------------------------------------------------

# 📈 Reporting

The reporting API:

``` text
GET /admin/reports
```

provides:

-   Donation summary
-   Status breakdown
-   Food-type breakdown
-   Total food portions
-   Completed food portions
-   Completion rate
-   Donor and receiver counts

------------------------------------------------------------------------

# 📤 CSV Export

Administrators can export donation information as CSV.

CSV export can be used for:

-   Data analysis
-   Operational reports
-   Project demonstrations
-   Portfolio presentation

------------------------------------------------------------------------

# 🔐 Security

Security was considered throughout the application.

### Authentication

Amazon Cognito manages user authentication.

### Authorization

API Gateway validates JWT tokens and Lambda functions enforce
application roles.

### IAM

AWS IAM controls access between Lambda and AWS services.

### Input Validation

The backend validates donation fields such as:

-   Food type
-   Quantity
-   Pickup location
-   Pickup time
-   Description
-   Donation ID
-   Status

### Secrets

Sensitive configuration is stored outside the source code.

The Streamlit Amazon Location API key is stored in:

``` text
.streamlit/secrets.toml
```

This file must never be committed to GitHub.

------------------------------------------------------------------------

# 📈 Monitoring

Amazon CloudWatch is used for application monitoring.

### Lambda Logs

Lambda execution logs are stored in CloudWatch Logs.

### Log Retention

Lambda log groups are configured with a **30-day retention period**.

### CloudWatch Alarms

The project includes alarms for:

-   Create Donation Lambda errors
-   API Gateway 5XX errors

The alarms publish notifications through the RescueLink SNS topic.

------------------------------------------------------------------------

# 🧰 Technology Stack

### Frontend

``` text
Python
Streamlit
Requests
Boto3
```

### Backend

``` text
Python
AWS Lambda
Amazon API Gateway
```

### Database

``` text
Amazon DynamoDB
```

### Authentication

``` text
Amazon Cognito
```

### Automation

``` text
Amazon EventBridge
```

### Notifications

``` text
Amazon SNS
```

### Location

``` text
Amazon Location Service
```

### Monitoring

``` text
Amazon CloudWatch
```

### Security

``` text
AWS IAM
Cognito JWT Authorization
API Gateway JWT Authorizer
```

------------------------------------------------------------------------

# 📁 Project Structure

``` text
RescueLink-Frontend/
│
├── .streamlit/
│   └── secrets.toml
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── venv/
```

------------------------------------------------------------------------

# 🖥️ Local Setup

## Prerequisites

Install:

-   Python 3.x
-   Git
-   AWS account
-   Required AWS resources
-   Streamlit

------------------------------------------------------------------------

## 1. Clone the Repository

``` bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd RescueLink-Frontend
```

## 2. Create Virtual Environment

``` powershell
python -m venv venv
```

## 3. Activate Virtual Environment

``` powershell
.\venv\Scripts\Activate.ps1
```

## 4. Install Dependencies

``` powershell
pip install -r requirements.txt
```

## 5. Configure Secrets

Create:

``` text
.streamlit/secrets.toml
```

Add:

``` toml
AWS_LOCATION_API_KEY = "YOUR_API_KEY"
```

Never commit this file.

## 6. Run the Application

``` powershell
streamlit run app.py
```

------------------------------------------------------------------------

# ⚙️ Configuration

The application requires the following configuration:

``` text
API Gateway URL
Cognito User Pool
Cognito App Client
Amazon Location API Key
```

Sensitive values should be stored in Streamlit secrets or environment
variables rather than hard-coded in the source code.

------------------------------------------------------------------------

# 🌎 AWS Regions

The primary RescueLink application resources are deployed in:

``` text
ap-south-2
```

This includes the main:

-   Lambda functions
-   API Gateway
-   DynamoDB
-   Cognito
-   EventBridge
-   SNS
-   CloudWatch resources

Amazon Location Service resources are configured in:

``` text
ap-south-1
```

because the required Location Service functionality is not available in
the primary application region.

------------------------------------------------------------------------

# 🧪 Testing

The following workflows have been tested:

### Authentication

-   Cognito login
-   JWT authentication
-   Role detection
-   Protected API access
-   Unauthorized access handling

### Donations

-   Donation creation
-   Donation listing
-   Donation retrieval
-   Donation claiming
-   Status updates
-   Donation completion
-   Donation cancellation
-   Automatic expiry

### Role Testing

``` text
DONOR
RECEIVER
ADMIN
```

Role-specific permissions are enforced by the backend.

### Notifications

Tested:

``` text
Donation Claimed
Donation Picked Up
Donation Completed
```

### Admin

Tested:

-   Admin dashboard
-   Donation statistics
-   User listing
-   Donation listing
-   Reports
-   Status breakdown
-   Food-type breakdown
-   CSV export

### Location

Tested:

-   Address search
-   Geocoding
-   Coordinate retrieval
-   Map display

### Monitoring

Tested:

-   Lambda CloudWatch logs
-   API Gateway metrics
-   CloudWatch alarms

------------------------------------------------------------------------

# 🚀 Future Improvements

Possible future enhancements:

### 📱 SMS Notifications

Add SMS notifications using Amazon SNS.

### 📷 QR Code Pickup Verification

``` text
Donation
   │
   ▼
QR Code
   │
   ▼
Receiver Scans
   │
   ▼
Verification
   │
   ▼
PICKED_UP
```

### 🗺️ Advanced Maps

-   Nearby donations
-   Distance calculation
-   Route calculation
-   Pickup navigation
-   Donation markers

### 🤖 AI Food Classification

Allow donors to upload food images and classify the food automatically.

### 📊 Predictive Analytics

Use historical donation data to analyze:

-   Food surplus trends
-   Donation demand
-   High-demand locations
-   Donation patterns

### 🧠 Intelligent Matching

Automatically match donors and receivers using:

-   Food type
-   Quantity
-   Location
-   Distance
-   Pickup time
-   Demand

### 🌐 Public Impact Dashboard

Display metrics such as:

``` text
Total Donations
Food Rescued
Completed Pickups
Organizations Helped
Estimated Meals Rescued
```

### 🔄 CI/CD

Future deployment can use:

``` text
GitHub
   │
   ▼
CI/CD Pipeline
   │
   ▼
Automated Testing
   │
   ▼
AWS Deployment
```

------------------------------------------------------------------------

# 🎓 Learning Outcomes

This project demonstrates practical experience with:

-   AWS cloud architecture
-   Serverless application development
-   Python
-   Streamlit
-   REST APIs
-   API Gateway
-   AWS Lambda
-   DynamoDB
-   Amazon Cognito
-   JWT authentication
-   Role-based authorization
-   Event-driven architecture
-   Amazon EventBridge
-   Amazon SNS
-   Amazon Location Service
-   Amazon CloudWatch
-   AWS IAM
-   NoSQL database design
-   Input validation
-   Monitoring
-   Cloud security
-   Reporting
-   CSV export

------------------------------------------------------------------------

# 💼 Resume Description

### RescueLink --- Serverless Food Redistribution Platform

-   Built a serverless food redistribution platform using **AWS Lambda,
    API Gateway, DynamoDB, Amazon Cognito, EventBridge, SNS, CloudWatch,
    and Amazon Location Service**.
-   Developed a **Python Streamlit frontend** supporting DONOR,
    RECEIVER, and ADMIN roles with JWT-based authentication and
    role-based authorization.
-   Implemented the donation lifecycle from **AVAILABLE → CLAIMED →
    PICKED_UP → COMPLETED**, including automatic expiration of outdated
    donations.
-   Developed an event-driven notification system using **Amazon
    EventBridge and Amazon SNS**.
-   Built an administrative dashboard with **donation analytics, status
    breakdowns, food-type statistics, completion rates, and CSV
    export**.
-   Integrated **Amazon Location Service** for address search and
    geocoding.
-   Added **CloudWatch monitoring and error alarms** for application
    reliability.

------------------------------------------------------------------------

# 📝 Portfolio Description

**RescueLink is a serverless AWS food redistribution platform built with
Python and Streamlit that connects food donors with charities,
volunteers, and receivers. The application uses Amazon Cognito, API
Gateway, Lambda, DynamoDB, EventBridge, SNS, Amazon Location Service,
CloudWatch, and IAM to provide secure authentication, role-based
donation management, automated expiry, event-driven notifications,
location services, administrative analytics, and monitoring.**

------------------------------------------------------------------------

# ⭐ Project Highlights

``` text
🍱 Food Redistribution
☁️ Serverless AWS Architecture
🐍 Python + Streamlit
🔐 Cognito Authentication
👥 Role-Based Access Control
⚡ Event-Driven Architecture
📧 Email Notifications
⏰ Automatic Donation Expiry
📍 Amazon Location Service
📊 Admin Analytics
📤 CSV Reporting
📈 CloudWatch Monitoring
🗄️ DynamoDB
```

------------------------------------------------------------------------

# 📸 Screenshots

Recommended screenshots for the GitHub repository:

1.  Login page
2.  Donor dashboard
3.  Create Donation page
4.  Available Donations
5.  Receiver dashboard
6.  Claim workflow
7.  Admin dashboard
8.  Admin reports
9.  Location map
10. AWS architecture
11. CloudWatch monitoring

Example:

``` markdown
![RescueLink Dashboard](screenshots/dashboard.png)
```

------------------------------------------------------------------------

# 🏆 Interview Discussion Points

The project can be discussed during interviews around:

### Serverless Architecture

Why Lambda and API Gateway were selected instead of traditional servers.

### DynamoDB

Why a NoSQL database was selected and how the partition/sort key
structure works.

### Cognito

How authentication and JWT authorization work.

### IAM

How Lambda permissions are controlled.

### EventBridge

Why event-driven architecture was used for notifications and scheduled
expiry.

### SNS

How email notifications are delivered.

### CloudWatch

How application errors and Lambda executions are monitored.

### Amazon Location Service

How addresses are converted into geographic coordinates.

### Role-Based Access

How DONOR, RECEIVER, and ADMIN permissions are enforced.

------------------------------------------------------------------------

# 📌 Project Status

``` text
✅ Authentication
✅ Role-Based Authorization
✅ Donation Creation
✅ Donation Listing
✅ Donation Claiming
✅ Donation Status Management
✅ Automatic Donation Expiry
✅ EventBridge Automation
✅ SNS Notifications
✅ Admin Dashboard
✅ Admin User Management
✅ Admin Donation Management
✅ Admin Reporting
✅ CSV Export
✅ Amazon Location Geocoding
✅ CloudWatch Logs
✅ CloudWatch Alarms
✅ Secret Protection
```

------------------------------------------------------------------------

# 👨‍💻 Author

## Moushik Shaik

**AWS / Cloud / Python Developer**

RescueLink was developed as a practical AWS portfolio project to
demonstrate real-world serverless application development and cloud
engineering skills.

------------------------------------------------------------------------

# 📄 License

This project is intended for educational, portfolio, and demonstration
purposes.

------------------------------------------------------------------------

# ⭐ RescueLink

### Connecting surplus food with people who need it.

``` text
DONATE → CLAIM → PICK UP → COMPLETE
```
