from flask_smorest import Blueprint, abort
from flask.views import MethodView
from typing import Any, Dict

from ..models import create_task, list_tasks, get_task, update_task, delete_task
from ..schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema

blp = Blueprint(
    "Tasks",
    "tasks",
    url_prefix="/tasks",
    description="Endpoints to manage to-do tasks (CRUD).",
)

@blp.route("/")
class TasksListResource(MethodView):
    # PUBLIC_INTERFACE
    def get(self):
        """List all tasks."""
        tasks = list_tasks()
        return tasks, 200

    # PUBLIC_INTERFACE
    @blp.arguments(TaskCreateSchema)
    @blp.response(201, TaskSchema)
    def post(self, data: Dict[str, Any]):
        """Create a new task."""
        title = data["title"]
        completed = bool(data.get("completed", False))
        task = create_task(title=title, completed=completed)
        return task

@blp.route("/<int:task_id>")
class TaskResource(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, TaskSchema)
    def get(self, task_id: int):
        """Retrieve a single task by ID."""
        task = get_task(task_id)
        if not task:
            abort(404, message="Task not found")
        return task

    # PUBLIC_INTERFACE
    @blp.arguments(TaskUpdateSchema)
    @blp.response(200, TaskSchema)
    def put(self, data: Dict[str, Any], task_id: int):
        """Update a task (title and/or completed)."""
        updated = update_task(task_id, title=data.get("title"), completed=data.get("completed"))
        if not updated:
            abort(404, message="Task not found")
        return updated

    # PUBLIC_INTERFACE
    def delete(self, task_id: int):
        """Delete a task by ID."""
        ok = delete_task(task_id)
        if not ok:
            abort(404, message="Task not found")
        return {"message": "Task deleted"}, 200
