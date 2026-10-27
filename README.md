# Falcon Vision

## Executive Overview

**Falcon Vision** is an AI-powered industrial safety monitoring platform that pairs computer vision (CV) with natural language processing (NLP) to dynamically enforce workplace safety standards.

Unlike conventional, static computer vision systems that rely strictly on predefined rules, Falcon Vision allows organizations to upload proprietary **PDF safety regulation documents**. The system parses these documents using Large Language Models (LLMs) to extract organization-specific safety directives (such as mandatory PPE, access restriction rules, and environmental monitoring thresholds) and dynamically configures its AI detection pipeline accordingly.

```
                  +-----------------------------------+
                  |   Organization Safety PDF         |
                  +-----------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------+
|               backend/ - LLM Rule Extraction                      |
|      (Converts raw PDF text into active system rules)             |
+-------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------+
|               Dynamic AI Edge Monitoring Pipeline                  |
|  +------------------+ +------------------+ +-------------------+  |
|  |  PPE Detection   | | Fall Detection   | | Fire & Smoke      |  |
|  |   (YOLO Object)  | |  (Pose Estim.)   | | (YOLO Vision)   |  |
|  +------------------+ +------------------+ +-------------------+  |
|  +-------------------------------------------------------------+  |
|  |         Face Recognition & Access Control (ONNX)            |  |
|  +-------------------------------------------------------------+  |
+-------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------+
|               frontend/ - Dashboard & Real-Time Alerts             |
|          (React / TypeScript / Vite / Real-time Bounding Boxes)   |
+-------------------------------------------------------------------+

```

---

## Technical Architecture & Tech Stack

### Frontend Stack (`frontend/`)

* **Core Framework:** React 18, TypeScript, Vite
* **State & Routing:** React Router
* **Styling & UI:** Tailwind CSS, Lucide React Icons
* **Data Visualization & UX:** Recharts (Analytics & Monitoring Reports), Sonner (Toast Notifications)

### Backend Stack (`backend/`)

* **API Framework:** Python 3.10+, FastAPI (Asynchronous API endpoints)
* **Database & ORM:** MongoDB via Motor (Async driver) / PyMongo, structured using Pydantic schemas
* **Authentication:** JWT (JSON Web Tokens) with granular Role-Based Access Control (RBAC: Admin vs. Supervisor) and strict password hashing

### AI, ML & Computer Vision Frameworks

* **Vision Models:** Ultralytics YOLO (`.pt` formats for object, fire, and smoke detection)
* **Inference Engines:** ONNX Runtime, scikit-learn (Random Forest fall classification: `fall_classifier_RF.pkl`), OpenCV, NumPy
* **Document Processing & Parsing:** PDF extraction combined with LLM-assisted rule extraction (featuring local fallback mechanisms for offline/air-gapped industrial deployment)

---

## Core Operational Workflows

```
  +---------------+        +----------------------+        +-----------------------+
  |  1. PDF Upload | -----> | 2. Rule Extraction   | -----> | 3. Rule Activation    |
  |  (Admin)      |        |    (LLM Pipeline)     |        |    (Admin Selection)  |
  +---------------+        +----------------------+        +-----------------------+
                                                                       |
  +---------------+        +----------------------+                    |
  | 5. Alerts &   | <----- | 4. Frame Processing  | <------------------+
  |    Reports    |        |    (Supervisor Live) |
  +---------------+        +----------------------+

```

### 1. Dynamic Rule Extraction Workflow

1. An **Admin** uploads an official Safety Standard PDF.
2. The `LLM/` module processes the raw text and extracts structured requirements covering required PPE, fall hazards, fire risks, and restricted access profiles.
3. Extracted rules are mapped into database schemas. Admins review, toggle, and activate specific rules or module overrides.
4. Active rules dynamically update the bounding-box logic and threshold checks executed during live monitoring.

### 2. Multi-Modal Vision & Detection Pipeline

* **PPE Compliance (`PPE/`):** Detects 10+ items including helmets, safety vests, boots, gloves, masks, face shields, glasses, coveralls, ear protection, and safety harnesses. Compares frame detections against the mandatory list required by the currently active regulation.
* **Fall Detection (`Fall model/`):** Combines pose estimation with a Random Forest classifier (`fall_classifier_RF.pkl`) to evaluate spatial orientation and human keypoint angles for sudden elevation or position anomalies.
* **Fire & Smoke Hazard Identification (`Fire Detection/`):** Runs dedicated fine-tuned YOLO instances (`fire_model.pt`) to detect combustion and smoke presence across video channels.
* **Access Control & Face Recognition (`Face Recognition/`):** Compares faces detected in monitored zones against an employee facial embedding database, flagging unidentified or unauthorized personnel in real time.

---

## User Roles & Capabilities

| Capability | Admin Role | Supervisor Role |
| --- | --- | --- |
| **Organization Management** (Signup, Settings, RBAC) | Direct Access | Restricted |
| **Regulation Upload & Rule Parsing** | Direct Access | View Only |
| **Employee & Face Gallery Management** | Direct Access | View Only |
| **Live Camera Monitoring & Bounding Box View** | Full Access | Full Access |
| **Alert History Management & Deletion** | Clear/Delete/View | View Only |
| **Session Report Generation & Export** | Full Access | Full Access |

---

## Repository Directory Layout

```
Falcon-Vision/
├── backend/                  # FastAPI web server, database abstractions, auth, & AI service adapters
├── frontend/                 # Vite-powered React UI, web dashboards, & live player controls
├── PPE/                      # PPE detection training assets and model weights (PPE_model.pt)
├── Fall model/               # Fall detection models (fall_model.pt, fall_classifier_RF.pkl)
├── Fire Detection/           # Fire & smoke vision models (fire_model.pt)
├── Face Recognition/         # Face embedding extraction notebooks & ONNX wrappers
└── LLM/                      # PDF rule extraction notebooks and LLM fallback scripts

```

---

## System Key Highlights

* **Adaptive Safety Enforcements:** Replaces static rule sets with dynamic PDF ingestion—enabling different facilities or departments to run customized safety protocols without rebuilding code.
* **Multi-Hazard Visual Engine:** Parallel processing of PPE compliance, posture analysis, thermal/smoke hazards, and personnel authorization within a single integrated stream interface.
* **Audit-Ready Evidence Storage:** Automatically tags alerts with categorical severity ratings, timestamps, zone locations, and saved frame screenshots for legal compliance and post-incident investigations.
