from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    id = fields.Int(dump_only=True, metadata={"description": "Unique identifier for the task"})
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=250),
        metadata={"description": "Title or description of the task"},
    )
    completed = fields.Bool(
        required=True,
        metadata={"description": "Completion status of the task"},
    )

class TaskCreateSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=250),
        metadata={"description": "Title or description of the task"},
    )
    completed = fields.Bool(
        required=False,
        load_default=False,
        metadata={"description": "Initial completion status (default false)"},
    )

class TaskUpdateSchema(Schema):
    title = fields.Str(
        required=False,
        validate=validate.Length(min=1, max=250),
        metadata={"description": "Updated title"},
    )
    completed = fields.Bool(
        required=False,
        metadata={"description": "Updated completion status"},
    )
