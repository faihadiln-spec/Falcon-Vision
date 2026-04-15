from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.api.deps import get_current_user, get_employee_service
from app.schemas.employee_schema import (
    EmployeeCreateRequest,
    EmployeeListResponse,
    EmployeeResponse,
    EmployeeUpdateRequest,
)
from app.services.employee_service import EmployeeService


router = APIRouter()


@router.post("", response_model=EmployeeResponse, status_code=201)
async def create_employee(
    request: EmployeeCreateRequest,
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> EmployeeResponse:
    return await employee_service.create_employee(request, current_user)


@router.get("", response_model=EmployeeListResponse)
async def list_employees(
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> EmployeeListResponse:
    return await employee_service.list_employees(current_user)


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: str,
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> EmployeeResponse:
    return await employee_service.get_employee(employee_id, current_user)


@router.patch("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: str,
    request: EmployeeUpdateRequest,
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> EmployeeResponse:
    return await employee_service.update_employee(employee_id, request, current_user)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_employee(
    employee_id: str,
    employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Response:
    await employee_service.delete_employee(employee_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
