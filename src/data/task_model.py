import time
from random import randint, choice, sample
from pydantic import BaseModel, Field
from typing import List
from faker import Faker


class TaskModel(BaseModel):
    name: str
    description: str | None = None
    assignees: List[int] | None = None
    archived: bool | None = None
    group_assignees: List[str] | None = None
    tags: List[str] | None = None
    status: str | None = None
    priority: int | None = None
    due_date: int | None = None
    due_date_time: bool | None = None
    time_estimate: int | None = None
    start_date: int | None = None
    start_date_time: bool | None = None
    points: int | None = None
    notify_all: bool | None = None
    parent: str | None = Field(default=None, description="Указать task ID родительской задачи")
    markdown_content: str | None = Field(default=None, description="Если указан - заменяет значение поля description")
    links_to: str | None = Field(default=None,
        description="Include a task ID to create a linked dependency with your new task.")
    check_required_custom_fields: bool | None = Field(default=None,
        description="Ignore checked required fields: false (default). Check required fields: true.")
    custom_item_id: int | None = None
    huevo_pole: str|None=None

    @classmethod
    def gen_fake_data(cls):
        STATUSES = ["TO DO", "In Progress", "Ready to start Testing", "Testing", "Ready to Deploy", "Done", "Blocked"]
        fake = Faker()
        return TaskModel(
            name=fake.catch_phrase(),
            description=fake.sentence(8),
            assignees=sample(range(1000, 10000), randint(1, 9)),
            archived=fake.boolean(),
            group_assignees=[fake.uuid4() for _ in range(randint(1, 9))],
            tags=[fake.bs().replace(" ", "_") for _ in range(randint(0, 3))],
            status=choice(STATUSES),
            priority=randint(1, 4),
            due_date=randint(int(time.time() * 1000), int(time.time() * 1000) + 61 * 24 * 60 * 60 * 1000),
            due_date_time=fake.boolean(),
            time_estimate=randint(1 * 60 * 60 * 1000, 24 * 60 * 60 * 1000),
            start_date=randint(int(time.time() * 1000) - 61 * 24 * 60 * 60 * 1000, int(time.time() * 1000)),
            start_date_time=fake.boolean(),
            # points=randint(0, 3),
            notify_all=fake.boolean()
        )

    @classmethod
    def gen_required_field(cls):
        fake = Faker()
        return TaskModel(
            name=fake.catch_phrase()
        )
