from http.client import HTTPException
from typing import List, Optional
from datamodel.models import Interaction, Patient
from fastapi import FastAPI, HTTPException, Query
from utils.data_utils import DataUtils
from utils.injectors import sql_instance
from fastapi.responses import JSONResponse
import mysql.connector
from mysql.connector import MySQLConnection
from contextlib import asynccontextmanager

connection: MySQLConnection = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for managing the lifespan of the database connection.
    """
    global connection
    connection = sql_instance()
    yield

    if connection and connection.connected:
        connection.close()
        print("Database connection closed")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    """
    Root endpoint returning a simple message.
    """
    return {"msg": "Hello World"}


@app.post("/interactions/")
def create_interactions(interaction: Interaction):
    """
    Endpoint to create patient interactions.

    Args:
        interaction (Interaction): The interaction data to be inserted.

    Returns:
        JSONResponse: JSON response with a success message or error details.
    """

    data_utils = DataUtils(connection)
    if not data_utils.get_patient_by_insurance_no(interaction.insurance_no):
        raise HTTPException(status_code=404, detail="Patient record does not exist")
    try:
        data_utils.insert_interactions([interaction])
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error creating interactions" + str(e)
        )
    return JSONResponse(
        status_code=201, content={"message": "Patient Interaction created successfully"}
    )


@app.get(
    "/interactions/{insurance_no}/", status_code=200, response_model=List[Interaction]
)
def get_interactions(
    insurance_no: str,
    labels: Optional[str] = None,
    offset: int = Query(
        0,
        ge=0,
        description="The number of items to skip before starting to collect the result set",
    ),
    limit: int = Query(10, gt=0, le=100, description="The numbers of items to return"),
):

    """
    Endpoint to retrieve interactions for a specific insurance number.

    Args:
        insurance_no (str): Insurance number of the patient.
        labels (Optional[str], optional): Filter interactions by label. Defaults to None.
        offset (int, optional): Number of items to skip. Defaults to 0.
        limit (int, optional): Number of items to return. Defaults to 10.

    Returns:
        List[Interaction]: List of Interaction objects matching the criteria.
    """
    data_utils = DataUtils(connection)
    if not data_utils.get_patient_by_insurance_no(insurance_no):
        raise HTTPException(status_code=404, detail="Patient record does not exist")
    try:
        interactions = data_utils.get_interaction_info(
            insurance_no=insurance_no, labels=labels, offset=offset, limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error fetching interactions details" + str(e)
        )
    return interactions


@app.get("/patient/{insurance_no}/", status_code=200, response_model=List[Patient])
def get_patient_info(insurance_no: str):
    """
    Endpoint to retrieve patient information by insurance number.

    Args:
        insurance_no (str): Insurance number of the patient.

    Returns:
        List[Patient]: List of Patient objects matching the insurance number.
    """
    data_utils = DataUtils(connection)

    try:
        patient_info = data_utils.get_patient_by_insurance_no(insurance_no)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error fetching patient details" + str(e)
        )
    if not patient_info:
        raise HTTPException(status_code=404, detail="Patient record does not exist")
    return patient_info
