"""
Endpoints de tarefas
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import structlog

from app.core.security import get_current_user, require_operator
from app.models.task import TaskStatus, TaskPriority
from app.services.task_service import TaskService

logger = structlog.get_logger()
router = APIRouter()

class TaskCreate(BaseModel):
    """Criar tarefa"""
    title: str
    description: Optional[str] = None
    natural_command: str
    priority: TaskPriority = TaskPriority.MEDIUM

class TaskUpdate(BaseModel):
    """Atualizar tarefa"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

class TaskResponse(BaseModel):
    """Resposta de tarefa"""
    id: int
    title: str
    description: Optional[str]
    natural_command: str
    status: TaskStatus
    priority: TaskPriority
    execution_plan: Optional[dict]
    requires_approval: bool
    estimated_duration: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: int

class TaskList(BaseModel):
    """Lista de tarefas"""
    tasks: List[TaskResponse]
    total: int
    page: int
    per_page: int

@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user)
):
    """Criar nova tarefa"""
    try:
        logger.info("Criando nova tarefa", 
                   user_id=current_user["id"], 
                   title=task.title)
        
        task_service = TaskService()
        new_task = await task_service.create_task(task, current_user["id"])
        
        logger.info("Tarefa criada com sucesso", 
                   task_id=new_task.id,
                   user_id=current_user["id"])
        
        return new_task
        
    except Exception as e:
        logger.error("Erro ao criar tarefa", 
                    user_id=current_user["id"], 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar tarefa: {str(e)}"
        )

@router.get("/", response_model=TaskList)
async def list_tasks(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    current_user: dict = Depends(get_current_user)
):
    """Listar tarefas"""
    try:
        task_service = TaskService()
        tasks = await task_service.list_tasks(
            user_id=current_user["id"],
            page=page,
            per_page=per_page,
            status=status,
            priority=priority
        )
        
        return tasks
        
    except Exception as e:
        logger.error("Erro ao listar tarefas", 
                    user_id=current_user["id"], 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar tarefas"
        )

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Obter tarefa específica"""
    try:
        task_service = TaskService()
        task = await task_service.get_task(task_id, current_user["id"])
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        
        return task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Erro ao buscar tarefa", 
                    task_id=task_id,
                    user_id=current_user["id"], 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar tarefa"
        )

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Atualizar tarefa"""
    try:
        task_service = TaskService()
        updated_task = await task_service.update_task(
            task_id, 
            task_update, 
            current_user["id"]
        )
        
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        
        logger.info("Tarefa atualizada", 
                   task_id=task_id,
                   user_id=current_user["id"])
        
        return updated_task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Erro ao atualizar tarefa", 
                    task_id=task_id,
                    user_id=current_user["id"], 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar tarefa"
        )

@router.post("/{task_id}/approve")
async def approve_task(
    task_id: int,
    current_user: dict = Depends(require_operator)
):
    """Aprovar tarefa para execução"""
    try:
        task_service = TaskService()
        approved_task = await task_service.approve_task(task_id, current_user["id"])
        
        if not approved_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        
        logger.info("Tarefa aprovada", 
                   task_id=task_id,
                   approver_id=current_user["id"])
        
        return {"message": "Tarefa aprovada com sucesso", "task_id": task_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Erro ao aprovar tarefa", 
                    task_id=task_id,
                    user_id=current_user["id"], 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao aprovar tarefa"
        )

@router.post("/{task_id}/execute")
async def execute_task(
    task_id: int,
    current_user: dict = Depends(require_operator)
):
    """Executar tarefa aprovada"""
    try:
        task_service = TaskService()
        execution_result = await task_service.execute_task(task_id, current_user["id"])
        
        logger.info("Execução de tarefa iniciada", 
                   task_id=task_id,
                   executor_id=current_user["id"])
        
        return execution_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Erro ao executar tarefa", 
                    task_id=task_id,
                    user_id=current_user["id"], 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao executar tarefa"
        )

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Cancelar/deletar tarefa"""
    try:
        task_service = TaskService()
        deleted = await task_service.delete_task(task_id, current_user["id"])
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        
        logger.info("Tarefa deletada", 
                   task_id=task_id,
                   user_id=current_user["id"])
        
        return {"message": "Tarefa deletada com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Erro ao deletar tarefa", 
                    task_id=task_id,
                    user_id=current_user["id"], 
                    error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar tarefa"
        )
