# fhir-observation-ingestion-api

A FastAPI-based service for validating and ingesting FHIR R4 Observation resources with FHIR-compliant responses.

## Overview

This project implements a lightweight batch ingestion pipeline that accepts FHIR `Observation` resources, performs structural validation using official FHIR R4 models, and returns a standards-compliant `OperationOutcome` summarizing successes and failures.

## Features

- Batch ingestion of FHIR Observation resources
- Structural validation using FHIR R4 models
- FHIR-compliant `OperationOutcome` responses
- Per-resource success and error reporting
- Interactive API documentation via FastAPI

## Tech Stack

- Python
- FastAPI
- Pydantic
- fhir.resources (FHIR R4)

## API Endpoints

### `POST /api/data-pipeline/ingest/Observation`
Accepts a list of FHIR Observation resources and returns a FHIR `OperationOutcome` detailing validation results.

### `GET /`
Health check endpoint.

## Running Locally

```bash
pip install fastapi uvicorn fhir.resources
uvicorn app:app --reload
