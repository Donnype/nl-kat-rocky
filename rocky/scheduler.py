import datetime
from enum import Enum
from typing import List, Optional, Any, Dict, Set, Union

import requests
from pydantic import BaseModel, Field

from tools.apps import scheduler_app

import scheduler
from scheduler import context, models, queues, schedulers
from scheduler.server.pagination import PaginatedResponse, paginate


class Boefje(BaseModel):
    """Boefje representation."""

    id: str
    name: Optional[str]
    description: Optional[str]
    repository_id: Optional[str]
    version: Optional[str] = Field(default=None)
    scan_level: Optional[int] = Field(default=None)
    consumes: Optional[Union[str, Set[str]]]
    produces: Optional[Set[str]]


class BoefjeMeta(BaseModel):
    """BoefjeMeta is the response object returned by the Bytes API"""

    id: str
    boefje: Boefje
    input_ooi: str
    arguments: Dict[str, Any]
    organization: str
    started_at: Optional[datetime.datetime]
    ended_at: Optional[datetime.datetime]


class Normalizer(BaseModel):
    """Normalizer representation."""

    id: Optional[str]
    name: Optional[str]
    version: Optional[str] = Field(default=None)


class NormalizerTask(BaseModel):
    """NormalizerTask represent data needed for a Normalizer to run."""

    id: Optional[str]
    normalizer: Normalizer
    boefje_meta: BoefjeMeta


class BoefjeTask(BaseModel):
    """BoefjeTask represent data needed for a Boefje to run."""

    id: Optional[str]
    boefje: Boefje
    input_ooi: str
    organization: str


class QueuePrioritizedItem(BaseModel):
    """Representation of a queue.PrioritizedItem on the priority queue. Used
    for unmarshalling of priority queue prioritized items to a JSON
    representation.
    """

    priority: int
    item: Union[BoefjeTask, NormalizerTask]


class TaskStatus(Enum):
    """Status of a task."""

    PENDING = "pending"
    QUEUED = "queued"
    DISPATCHED = "dispatched"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    id: str
    hash: str
    scheduler_id: str
    task: QueuePrioritizedItem  # FIXME: p_item?
    status: TaskStatus
    created_at: datetime.datetime
    modified_at: datetime.datetime

    class Config:
        orm_mode = True


class PaginatedTasksResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Task]


class SchedulerClient:
    def __init__(self, *args, **kwargs):
        self.ctx = scheduler_app.ctx

    def list_tasks(self, queue_name: str, scheduler_id: Union[str, None] = None,
                   status: Union[str, None] = None,
                   offset: int = 0,
                   limit: int = 10,) -> PaginatedTasksResponse:
        results, count = self.ctx.datastore.get_tasks(
            scheduler_id=scheduler_id,
            status=status,
            offset=offset,
            limit=limit,
        )

        return paginate(results, count=count, offset=offset, limit=limit)

    def push_task(
        self, queue_name: str, prioritized_item: QueuePrioritizedItem
    ) -> None:
        s = scheduler_app.schedulers.get(queue_name)
        if s is None:
            raise Exception

        p_item = queues.PrioritizedItem(**prioritized_item.dict())
        if s.queue.item_type == models.BoefjeTask:
            p_item.item = models.BoefjeTask(**p_item.item)
        elif s.queue.item_type == models.NormalizerTask:
            p_item.item = models.NormalizerTask(**p_item.item)

        s.push_item_to_queue(p_item)

        return models.QueuePrioritizedItem(**p_item.dict())


class SchedulerClientV1:
    def __init__(self, base_uri: str):
        self.session = requests.Session()
        self._base_uri = base_uri

    def list_tasks(self, queue_name: str) -> PaginatedTasksResponse:
        res = self.session.get(f"{self._base_uri}/schedulers/{queue_name}/tasks")
        return PaginatedTasksResponse.parse_raw(res.text)

    def push_task(
        self, queue_name: str, prioritized_item: QueuePrioritizedItem
    ) -> None:
        res = self.session.post(
            f"{self._base_uri}/queues/{queue_name}/push", data=prioritized_item.json()
        )
        res.raise_for_status()
