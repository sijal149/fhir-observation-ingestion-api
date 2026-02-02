# app.py

from fastapi import FastAPI, HTTPException
from fhir.resources.observation import Observation
from fhir.resources.operationoutcome import OperationOutcome
from pydantic import ValidationError
from typing import List, Dict, Any
import json
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="FHIR Data Ingestion Pipeline Service (FHIR-Compliant Response)",
    description="Validates and simulates ingestion. Returns a FHIR-compliant response.",
    version="3.0.0"
)

# --- INGESTION ENDPOINT ---

@app.post("/api/data-pipeline/ingest/Observation")
async def ingest_fhir_observations(observations_data: List[Dict[str, Any]]):
    """
    Accepts a list of FHIR Observation resources. Returns a custom FHIR-compliant
    OperationOutcome detailing all successes and failures in the batch.
    """
    successful_count = 0
    failed_issues = []

    #processing each fhir incoming fhir resources in the batch
    for index, resource_dict in enumerate(observations_data):
        try:
            #check resourceType
            if resource_dict.get('resourceType') != 'Observation':
                raise ValueError("Resource missing or incorrect 'resourceType'.")
            #Pydantic/FHIR R4 Structural Validation
            Observation.parse_obj(resource_dict) 
            successful_count += 1
            failed_issues.append({
                "severity": "information",
                "code": "informational",
                "details": {"text": f"Index {index}: Observation validated and successfully ingested."},
            })
            
        except (ValueError, ValidationError) as e:
            # Extract specific validation errors if available
            error_text = f"Validation failed: {str(e)}"
            if isinstance(e, ValidationError):
                error_text = f"Validation failed. Errors: {json.dumps(json.loads(e.json()), indent=2)}"
            
            # Add a critical error issue to the list
            failed_issues.append({
                "severity": "error",
                "code": "structure",
                "details": {"text": f"Index {index}: Resource failed validation."},
                "diagnostics": error_text
            })

        except Exception as e:
            # Handle non-validation errors (e.g., database connection failure)
            failed_issues.append({
                "severity": "fatal",
                "code": "exception",
                "details": {"text": f"Index {index}: Pipeline execution failed. Error: {str(e)}"}
            })


    # 2. FINAL FHIR-COMPLIANT RESPONSE (OperationOutcome)
    
    # The FHIR R4 OperationOutcome resource
    final_outcome = OperationOutcome(
        issue=failed_issues,
        text={
            "status": "generated",
            "div": f"<div>Batch Ingestion Report: {successful_count} Successes, {len(failed_issues) - successful_count} Failures</div>"
        }
    )
    
    # Determine the final HTTP status code
    if len(failed_issues) == successful_count:
        # All passed, return a standard success code
        return final_outcome 
    else:
        # One or more failed, return a 400 Bad Request (The standard for validation errors)
        raise HTTPException(status_code=400, detail=json.loads(final_outcome.json()))


# --- ROOT ENDPOINT ---
@app.get("/")
def read_root():
    return {"message": "FHIR Data Ingestion Pipeline Service is running. Check /docs for interactive testing."}